import csv
from datetime import datetime, timedelta

import pyexcel
import pynetbox
from elasticsearch import Elasticsearch, NotFoundError
from collections import Counter
from operator import itemgetter

from config import ELK_USER, ELK_PASS, ELK_URL, IPAM_URL, IPAM_TOKEN
from utils.bodies import Body


class DataConnector(Body):
    def __init__(self, *args, **kwargs):
        self.es = self.connect_elk(quiet=True)

    def try_repeat(func):
        def wrapper(*args, **kwargs):
            count = 3
            while count:
                try:
                    return func(*args, **kwargs)
                except NotFoundError:
                    count = 0
                    print('Сервер перегружен, попробуйте позже!')
                except Exception as e:
                    print(e)
                    print('[bold magenta]ReConnect...[/bold magenta]')
                    count -= 1
        return wrapper

    def connect_ipam(self):
        print('Connecting to ipsm.mchs.ru')
        nb = pynetbox.api(
            IPAM_URL,
            token=IPAM_TOKEN
        )
        return nb

    def connect_elk(self, quiet=None):
        user = ELK_USER
        pssw = ELK_PASS
        url = ELK_URL

        es = Elasticsearch(
            [url],
            http_auth=(user, pssw),
            scheme='http',
            timeout=20
        )
        if not quiet:
            print('Connecting to ELK...')
        return es

    def get_data_from_ipam(self, ip, connect=None):  # noqa: C901
        if connect is None:
            nb = self.connect_ipam()
        else:
            nb = connect
        tenant = None
        region = None
        prefix = None
        aggregate = None
        try:
            q = nb.ipam.ip_addresses.get(address=ip)
        except:
            q = None
        try:
            prefix = nb.ipam.prefixes.get(q=ip)

        except:  # noqa: E722
            prefixes = nb.ipam.prefixes.filter(q=ip)
            for item in prefixes:
                if item['prefix'][:8] == '10.155.0':
                    continue
                prefix = item
                break
        try:
            aggregate = nb.ipam.aggregates.get(q=prefix.prefix)
        except:  # noqa: E722
            aggregate = nb.ipam.aggregates.get(q=ip)
        try:
            tenant = nb.tenancy.tenants.get(name=q.tenant)
        except:  # noqa: E722
            try:
                tenant_name = None
                for attr in aggregate:
                    if tenant_name is not None:
                        break
                    if 'tenant' in attr:
                        tenant_name = aggregate.tenant.name
                        break
                    else:
                        for attr in prefix:
                            if 'tenant' in attr:
                                tenant_name = prefix.tenant.name
                                break
                tenant = nb.tenancy.tenants.get(name=tenant_name)
            except:  # noqa: E722
                print('Учреждения не закреплено за адресом')
        if tenant:
            for address in nb.dcim.sites.filter(tenant_id=tenant.id):
                addresses = address
                if addresses.region is None:
                    continue
                else:
                    region = addresses.region
                    break
        if q is None:
            res = {
                'ip': ip,
                'region': region if region is not None else '-',
                'tenant': tenant if tenant is not None else '-',
                'prefix': prefix if prefix is not None else '-',
                'aggregate': aggregate if aggregate is not None else '-',
            }
        else:
            res = {
                'ip': ip,
                'region': region,
                'tenant': tenant,
                'prefix': prefix,
                'aggregate': aggregate,
            }
        return res

    def make_files(self, data, event_type, tenant=None, search_tenant=None):
        file_name = ''
        if tenant:
            file_name += tenant + '-'
        else:
            file_name += 'all-'
        if event_type:
            file_name += event_type + '-'

        now = datetime.now() - timedelta(hours=3)
        now.strftime("%d.%m.%Y %H:%M")
        file_name += now.strftime("%d.%m.%Y_%H:%M")

        file_name_csv = file_name + '.csv'
        with open(file_name_csv, 'w', newline='', encoding='utf-8') as f:
            # fieldnames = ['region', 'status', 'threat', 'source', 'target', 'tenant', 'timestamp']
            wr = csv.writer(f)
            wr.writerow(data['fieldnames'])
            ips_dict = {}
            for rec in data['source']:
                if rec[2] and search_tenant:
                    if not(rec[2] in ips_dict.keys()):
                        tenant_name = get_data_from_ipam(rec[2])
                        ips_dict[rec[2]] = str(tenant_name['tenant'])
                    rec.append(ips_dict[rec[2]])
                    rec[3], rec[4], rec[5], rec[6], rec[7] = rec[7], rec[3], rec[4], rec[5], rec[6]
                wr.writerow(rec)
        file_name_xls = file_name + '.xls'
        x_data = []
        x_data.append(data['fieldnames'])
        for rec in data['source']:
            x_data.append(rec)
        try:
            pyexcel.save_as(array=x_data, dest_file_name=file_name_xls)
        except Exception as e:
            print(e)

        return file_name_csv, file_name_xls

    @try_repeat
    def get_all_attacks(self):
        body = self.get_elk_request_body(all_attacks=True)
        try:
            data = self.es.search(index='kasper*', body=body, size=10000, request_timeout=40)
        except Exception as e:
            raise Exception(e)

        hits = data['hits']['hits']
        if not hits:
            return None
        arr = []
        for hit in hits:
            region = attack = attack_count = tenant = None
            date = hit['_source']['@timestamp'].split('.')[0]
            try:
                region = hit['_source']['region']
            except Exception as e:
                print('ERROR region: ', e)
            try:
                attack = hit['_source']['sd']['event']['p1']
            except Exception as e:
                print('ERROR attack_target_ip: ', e)
            arr.append(f"{region}, {attack}")
        counter = Counter(arr)
        q = sorted(counter.items(), key=lambda i: i[1], reverse=True)
        result = []
        for row in q:
            result.append(f"Регион: {row[0].split(',')[0]}\n"
                          f"Тип атаки:\n"
                          f"{row[0].split(',')[1]}\n"
                          f"Колличество атак: {row[1]}\n")
        return result

    @try_repeat
    def get_all_events(self, tenant=None):
        body = self.get_elk_request_body(events=True)
        try:
            data = self.es.search(index='logstash*', body=body, size=9000, request_timeout=40)
        except Exception as e:
            raise Exception(e)
        buckets = data['aggregations']['2']['buckets']
        if not buckets:
            print('No data')
        buckets = sorted(buckets, key=lambda x: x['doc_count'], reverse=True)
        arr = []
        ips_dict = {}
        for bucket in buckets:
            users_arr = []
            region = bucket['key']
            all_events_counts = bucket['doc_count']
            if all_events_counts < 30:
                continue
            for user in bucket['6']['buckets']:
                if user['doc_count'] <= 30 or (str(user['key']).upper() in ['USER', 'ADMIN'] and user['doc_count'] < 10):
                    continue
                users_arr.append([user['key'], user['7']['buckets'][0]['key'], user['doc_count']])
            message = f'Регион: {region}\n' \
                      f'Событий: {all_events_counts}\n'  # f'Код события: {event}\n' \
            users_arr = sorted(users_arr, key=itemgetter(2), reverse=True)
            if users_arr:
                for user in users_arr:
                    appended = ''
                    if user[1] != '-':
                        if not (user[1] in ips_dict.keys()):
                            tenant_name = self.get_data_from_ipam(user[1])
                            ips_dict[user[1]] = str(tenant_name['tenant'])
                        appended = f"{user[0]} ({user[1]}, {ips_dict[user[1]]}): *{user[2]}* попыток\n"
                    else:
                        appended = f"{user[0]}: *{user[2]}* попыток\n"
                    if appended:
                        message += appended
            arr.append(message)
        return arr[:10]

    @try_repeat
    def get_change_privilege_events(self):
        """
        Получить свсе события за 24 часа "Повышение привилегий" "
        """
        body = self.get_elk_request_body(previlege=True)
        try:
            data = self.es.search(index='logstash*', body=body, size=1000, request_timeout=40)
        except Exception as e:
            raise Exception(e)
        hits = data['hits']['hits']
        if not hits:
            return None
        result = {}
        for hit in hits:
            event_code = agent_name = region = message = username = group_name = user_description = None
            date = hit['_source']['@timestamp'].split('.')[0]
            region = hit['_source']['region']
            event_code = hit['_source']['event']['code']
            agent_name = hit['_source']['agent']['name']
            message = hit['_source']['short_message']
            username = hit['_source']['winlog']['event_data']['SubjectUserName']
            group_name = hit['_source']['winlog']['event_data']['TargetUserName']
            try:
                user_description = hit['_source']['winlog']['event_data']['MemberName']
            except:
                user_description = ''

            if region in result.keys():
                result[region].append([date, event_code, message, agent_name, username, group_name, user_description])
            else:
                result[region] = [[date, event_code, message, agent_name, username, group_name, user_description]]

        return result

    @try_repeat
    def get_vpo_events(self, tenant=None, days=None):
        """
        Получить свсе события за 24 часа только критических ВПО. Список критических ВПО в отдельном файле vpo.txt
        """
        if tenant:
            body = self.get_elk_request_body(tenant, vpo=True, days=days)
        else:
            body = self.get_elk_request_body(vpo=True)
        try:
            data = self.es.search(index='kasper*', body=body, size=1000, request_timeout=40)
        except Exception as e:
            raise Exception(e)
        hits = data['hits']['hits']
        if not hits:
            if tenant:
                return None, None
            return None
        cleared_vpo = []
        result = {}
        for hit in hits:
            try:
                ip = hostname = region = message = vpo = group_name = user_description = None
                date = hit['_source']['@timestamp'].split('.')[0].replace('T', ' ')
                message = hit['_source']['sd']['event']['etdn']
                region = hit['_source']['region']
                ip = hit['_source']['sd']['event']['hip']
                hostname = hit['_source']['sd']['event']['hdn']
                vpo = hit['_source']['sd']['event']['p5']
                path = hit['_source']['sd']['event']['p2']

                if str(message).strip() == 'Объект удален':
                    cleared_vpo.append(path)
                    continue
                if tenant:
                    if region in result.keys():
                        result[region].append([date, region, ip, hostname, vpo, path, message])
                    else:
                        result[region] = [[date, region, ip, hostname, vpo, path, message]]
                else:
                    if region in result.keys():
                        if ip in result[region]:
                            if hostname in result[region][ip]:
                                result[region][ip][hostname].append(vpo)
                            else:
                                result[region][ip].update({hostname: [vpo]})
                        else:
                            result[region].update({ip: {hostname: [vpo]}})
                    else:
                        result[region] = {
                            ip: {hostname: [vpo]}
                        }

            except Exception as e:
                print(e)
        for val in result.values():
            for num, event in enumerate(val):
                for cleared_path in cleared_vpo:
                    if cleared_path in event[5]:
                        val.pop(num)
                        num -= 1
        if tenant:
            if not result[tenant]:
                return "Clear", "Clear"
            fieldnames = ['Дата', 'Регион', 'IP-адрес источника', 'Имя АРМ-а', 'ВПО', 'Путь', 'Сообщение']
            data = {
                'fieldnames': fieldnames,
                'source': result[tenant]
            }
            return self.make_files(data, 'vpo', tenant)
        return result

    @try_repeat
    def get_stats(self):
        body = self.get_elk_request_body(stats=True)
        try:
            data = self.es.search(index='kasper*', body=body, size=10000, request_timeout=40)
        except Exception as e:
            raise Exception(e)

        hits = data['hits']['hits']
        if not hits:
            print()
        arr = []
        count_attacks = len(hits)
        regions = []
        sources = []
        targets = []
        for hit in hits:
            region = source_ip = target_ip = None
            region = hit['_source']['region']
            source_ip = hit['_source']['attack_source_ip']
            target_ip = hit['_source']['attack_target_ip']
            regions.append(region)
            sources.append(source_ip)
            targets.append(target_ip)
        count_regions = len(list(set(regions)))
        count_sources = len(list(set(sources)))
        count_targets = len(list(set(targets)))
        return count_regions, count_attacks, count_sources, count_targets

    @try_repeat
    def get_stats_event(self):
        body_arms, body = self.get_elk_request_body(stats_event=True)
        try:
            data = self.es.search(index='logstash*', body=body, size=100, request_timeout=40)
        except Exception as e:
            raise Exception(e)
        count_4624 = 0  # int(data['aggregations']['4']['buckets'][0]['doc_count'])
        count_4625 = int(data['aggregations']['4']['buckets'][1]['doc_count'])
        count_4627 = 0  # int(data['aggregations']['4']['buckets'][2]['doc_count'])
        try:
            data = self.es.search(index='logstash*', body=body_arms, size=100, request_timeout=40)
        except Exception as e:
            raise Exception(e)
        print()
        region_count = int(data['aggregations']['1']['value'])
        arms_count = int(data['aggregations']['2']['value'])

        return count_4624, count_4625, count_4627, region_count, arms_count
