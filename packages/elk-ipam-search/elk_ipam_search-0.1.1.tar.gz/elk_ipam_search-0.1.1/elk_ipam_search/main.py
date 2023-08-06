import re
from datetime import datetime
from time import sleep

from utils.connectors import DataConnector


class Events(DataConnector):

    def __init__(self, *args, **kwargs):
        super(Events, self).__init__(*args, **kwargs)
        self.now = datetime.now()
        self.top_events = None
        self.groups_privilege = None
        self.vpo = None
        self.count_regions = self.count_attacks = self.count_sources = self.count_targets = None
        self.message = f'*__Сводка событий безопасности на {self.now.strftime("%d.%m.%Y %H:%M")} за 24 часа:__*\n\n'

    def get_stat(self):
        try:
            self.table = self.get_all_attacks()
            sleep(0.5)
            self.top_events = self.get_all_events()
            sleep(0.5)
            self.groups_privilege = self.get_change_privilege_events()
            sleep(0.5)
            self.vpo = self.get_vpo_events()
            self.count_regions, self.count_attacks, self.count_sources, self.count_targets = self.get_stats()
            if self.count_regions == self.count_attacks == self.count_sources == self.count_targets == 0:
                self.message += f'Сетевых атак не обнаружено!\n\n'
        except Exception as e:
            print(e)
            return None

    def check_attacks(self):
        self.message += f"*События \"Сетевые атаки\":*\n" \
                   f"Учреждений с атаками: {self.count_regions}\n" \
                   f"Всего атак: {self.count_attacks}\n" \
                   f"Атакующих: {self.count_sources}\n" \
                   f"Атакованных: {self.count_targets}\n\n"
        for row in self.table:
            self.message += row + '\n'

    def check_events(self):
        count_4624, count_4625, count_4627, region_count, arms_count = self.get_stats_event()
        self.message += f"\n*События 4625 (неуспешный вход в систему):*\n" \
                        f"Учреждений : {region_count}\n" \
                        f"АРМов: {arms_count}\n" \
                        f"Событий с кодом 4625: {count_4625}\n\n"
        for row in self.top_events:
            self.message += row + '\n'

    def check_vpo(self):
        self.message += f"\n*События \"Обнаружен вредоносный объект\":*"
        for gu, data in self.vpo.items():
            self.message += f'\n*Регион: {gu}*\n'
            for _ip, _host in data.items():
                try:
                    for hostname, vpos in _host.items():
                            count_vpos = "".join(vpos) if len(vpos) == 1 else len(vpos)
                            self.message += f'АРМ: {hostname} ({_ip})\n' \
                                       f'Обнаружено ВПО: {str(count_vpos) + " видов(а)" if isinstance(count_vpos, int) else count_vpos}\n'
                except Exception as e:
                    print(e)

    def check_groups_privilege(self):
        try:
            user_name_reg = re.compile(r'[Cc][Nn]=[\[]?([\w\s\.\-\_]+)')
            self.message += f"\n\n*События \"Изменение привилегий\":*"
            for gu, data in self.groups_privilege.items():
                self.message += f'\n*Регион: {gu}*'
                for item in data:
                    state = None
                    if item[1] == 4728:
                        state = "Добавление пользователя"
                    elif item[1] == 4729:
                        state = "Удаление пользователя"
                    elif item[1] == 4727:
                        state = "Создана группа с поддержкой безопасности"
                    elif item[1] == 4730:
                        state = "Группа с поддержкой безопасности удалена"
                    self.message += f'\n{item[0].replace("T", " ")}: {item[1]} ({state if state else item[2]})\n' \
                               f'Кто: {item[4]}\n' \
                               f'Кого: {re.search(user_name_reg, item[6]).group(1) if item[6] else "-"}\n' \
                               f'Группа: {item[5]}\n\n'
        except Exception as e:
            print(e)

    def run(self):
        self.get_stat()
        if self.table:
            self.check_attacks()
        if self.top_events:
            self.check_events()
        if self.vpo:
            self.check_vpo()
        if self.groups_privilege:
            self.check_groups_privilege()
        return self.message


if __name__ == '__main__':
    data = Events()
    data.run()
