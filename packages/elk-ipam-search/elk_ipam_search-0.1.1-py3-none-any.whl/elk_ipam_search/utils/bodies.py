from datetime import datetime, timedelta


class Body:
    def get_date(self, sed=None, days=None):
        delta = 24 * int(days) if days else 24
        time_to = datetime.now() - timedelta(hours=3)
        if sed:
            time_at = time_to - timedelta(days=30)
            return time_at.strftime('%Y-%m-%dT%H:%M:00.000Z'), time_to.strftime('%Y-%m-%dT%H:%M:00.000Z')

        time_at = time_to - timedelta(hours=delta)
        return time_at.strftime('%Y-%m-%dT%H:%M:00.000Z'), time_to.strftime('%Y-%m-%dT%H:%M:00.000Z')

    def get_elk_request_body(self, tenant=None, all_attacks=None, stats=None, events=None, stats_event=None, gu_ad=None, ip=None,
                             sed=None, previlege=None, vpo=None, days=None):

        date_from, date_to = self.get_date(days=days) if days else self.get_date()
        if all_attacks:
            body = {
                "aggs": {
                    "2": {
                        "terms": {
                            "field": "region.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 10
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "sd.event.p1.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 10
                                },
                                "aggs": {
                                    "5": {
                                        "terms": {
                                            "field": "mchs_organisation.keyword",
                                            "order": {
                                                "_count": "desc"
                                            },
                                            "size": 10
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "exists": {
                                    "field": "attack_source_ip"
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": date_from,
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": [
                            {
                                "match_phrase": {
                                    "attack_source_ip.keyword": "0.0.0.0"
                                }
                            },
                            {
                                "match_phrase": {
                                    "attack_target_ip.keyword": "0.0.0.0"
                                }
                            }
                        ]
                    }
                }
            }
            return body
        elif sed:
            date_from, date_to = get_date(sed=True)
            body = {
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "unmapped_type": "boolean"
                        }
                    }
                ],
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "30m",
                            "time_zone": "Europe/Moscow",
                            "min_doc_count": 1
                        }
                    }
                },
                "stored_fields": [
                    "*"
                ],
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    },
                    {
                        "field": "docker.time",
                        "format": "date_time"
                    },
                    {
                        "field": "event.created",
                        "format": "date_time"
                    },
                    {
                        "field": "nextcloud.time",
                        "format": "date_time"
                    },
                    {
                        "field": "nginx.time_iso8601",
                        "format": "date_time"
                    },
                    {
                        "field": "snoopy.date_iso_8601",
                        "format": "date_time"
                    },
                    {
                        "field": "winlog.event_data.NewTime",
                        "format": "date_time"
                    },
                    {
                        "field": "winlog.event_data.PreviousTime",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "exists": {
                                    "field": "user_address"
                                }
                            },
                            {
                                "match_phrase": {
                                    "user_address": f"{ip}"
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                         "gte": date_from,
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": [
                            {
                                "match_phrase": {
                                    "user_agent": "Drupal Command"
                                }
                            }
                        ]
                    }
                }
            }
            return body
        elif gu_ad and tenant:
            print('Body: gu_ad and tenant')
            body = {
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "unmapped_type": "boolean"
                        }
                    }
                ],
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "30m",
                            "time_zone": "Europe/Moscow",
                            "min_doc_count": 1
                        }
                    }
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {
                    "user_logon_only": {
                        "script": {
                            "source": "if (doc.containsKey('winlog.event_data.TargetUserName.keyword') && !doc['winlog.event_data.TargetUserName.keyword'].empty) {\n    if (doc['winlog.event_data.TargetUserName.keyword'].value =~ /^.*\\$$/) {\n        return false;\n    } else {\n        return true;\n    }\n}\nreturn false;",
                            "lang": "painless"
                        }
                    },
                    "region_url": {
                        "script": {
                            "source": "if (doc.containsKey('region.keyword') && !doc['region.keyword'].empty) {\n    def region_value = doc['region.keyword'].value;    \n    return region_value;\n}\ndef region_value = '#';    \nreturn region_value;",
                            "lang": "painless"
                        }
                    }
                },
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    },
                    {
                        "field": "docker.time",
                        "format": "date_time"
                    },
                    {
                        "field": "event.created",
                        "format": "date_time"
                    },
                    {
                        "field": "nextcloud.time",
                        "format": "date_time"
                    },
                    {
                        "field": "nginx.time_iso8601",
                        "format": "date_time"
                    },
                    {
                        "field": "snoopy.date_iso_8601",
                        "format": "date_time"
                    },
                    {
                        "field": "winlog.event_data.NewTime",
                        "format": "date_time"
                    },
                    {
                        "field": "winlog.event_data.PreviousTime",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_phrase": {
                                    "event.code": 4625
                                }
                            },
                            {
                                "match_phrase": {
                                    "region": tenant
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": date_from,
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": [
                            {
                                "script": {
                                    "script": {
                                        "source": "boolean compare(Supplier s, def v) {return s.get() == v;}compare(() -> { if (doc.containsKey('winlog.event_data.TargetUserName.keyword') && !doc['winlog.event_data.TargetUserName.keyword'].empty) {\n    if (doc['winlog.event_data.TargetUserName.keyword'].value =~ /^.*\\$$/) {\n        return false;\n    } else {\n        return true;\n    }\n}\nreturn false; }, params.value);",
                                        "lang": "painless",
                                        "params": {
                                            "value": False
                                        }
                                    }
                                }
                            }
                        ]
                    }
                },
            }
        elif events:
            # dates = make_date(all_attacks=True)
            body = {
                "aggs": {
                    "2": {
                        "terms": {
                            "script": {
                                "source": "if (doc.containsKey('region.keyword') && !doc['region.keyword'].empty) {\n    def region_value = doc['region.keyword'].value;    \n    return region_value;\n}\ndef region_value = '#';    \nreturn region_value;",
                                "lang": "painless"
                            },
                            "order": {
                                "_key": "desc"
                            },
                            "value_type": "string",
                            "size": 20
                        },
                        "aggs": {
                            "6": {
                                "terms": {
                                    "field": "winlog.event_data.TargetUserName.keyword",
                                    "order": {
                                        "_key": "desc"
                                    },
                                    "size": 50
                                },
                                "aggs": {
                                    "7": {
                                        "terms": {
                                            "script": {
                                                "source": "if (doc.containsKey('winlog.event_data.IpAddress.keyword') && !doc['winlog.event_data.IpAddress.keyword'].empty) {\n    def ip_value = doc['winlog.event_data.IpAddress.keyword'].value;\n    return ip_value;\n}\ndef region_value = '-';    \nreturn region_value;",
                                                "lang": "painless"
                                            },
                                            "order": {
                                                "_key": "desc"
                                            },
                                            "value_type": "string",
                                            "size": 20
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "stored_fields": [
                    "*"
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_phrase": {
                                    "event.code": "4625"
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": date_from,
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": [
                            {
                                "script": {
                                    "script": {
                                        "source": "boolean compare(Supplier s, def v) {return s.get() == v;}compare(() -> { if (doc.containsKey('winlog.event_data.TargetUserName.keyword') && !doc['winlog.event_data.TargetUserName.keyword'].empty) {\n    if (doc['winlog.event_data.TargetUserName.keyword'].value =~ /^.*\\$$/) {\n        return false;\n    } else {\n        return true;\n    }\n}\nreturn false; }, params.value);",
                                        "lang": "painless",
                                        "params": {
                                            "value": False
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
            return body
        elif stats_event:
            # dates = make_date(all_attacks=True)
            body_arms = {
                "aggs": {
                    "1": {
                        "cardinality": {
                            "field": "region.keyword"
                        }
                    },
                    "2": {
                        "cardinality": {
                            "field": "winlog.event_data.WorkstationName.keyword"
                        }
                    }
                },
                "size": 0,
                "stored_fields": [
                    "*"
                ],
                "script_fields": {
                    "user_logon_only": {
                        "script": {
                            "source": "if (doc.containsKey('winlog.event_data.TargetUserName.keyword') && !doc['winlog.event_data.TargetUserName.keyword'].empty) {\n    if (doc['winlog.event_data.TargetUserName.keyword'].value =~ /^.*\\$$/) {\n        return true;\n    }\n}\nreturn false;",
                            "lang": "painless"
                        }
                    }
                },
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    },
                    {
                        "field": "docker.time",
                        "format": "date_time"
                    },
                    {
                        "field": "event.created",
                        "format": "date_time"
                    },
                    {
                        "field": "nextcloud.time",
                        "format": "date_time"
                    },
                    {
                        "field": "nginx.time_iso8601",
                        "format": "date_time"
                    },
                    {
                        "field": "snoopy.date_iso_8601",
                        "format": "date_time"
                    },
                    {
                        "field": "winlog.event_data.NewTime",
                        "format": "date_time"
                    },
                    {
                        "field": "winlog.event_data.PreviousTime",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "script": {
                                                "script": {
                                                    "source": "boolean compare(Supplier s, def v) {return s.get() == v;}compare(() -> { if (doc.containsKey('winlog.event_data.TargetUserName.keyword') && !doc['winlog.event_data.TargetUserName.keyword'].empty) {\n    if (doc['winlog.event_data.TargetUserName.keyword'].value =~ /^.*\\$$/) {\n        return true;\n    }\n}\nreturn false; }, params.value);",
                                                    "lang": "painless",
                                                    "params": {
                                                        "value": False
                                                    }
                                                }
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "match_phrase": {
                                                "event.code": "4625"
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "match_phrase": {
                                    "type": "dc"
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": date_from,
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
            body = {
                "aggs": {
                    "4": {
                        "terms": {
                            "field": "winlog.event_id",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 6
                        }
                    }
                },
                "size": 0,
                "stored_fields": [
                    "*"
                ],
                "script_fields": {
                    "_user_logon_only": {
                        "script": {
                            "source": "if (doc['winlog.event_data.TargetUserName.keyword'].size() > 0) {\n    def m = /([a-zA-Z0-9-]+)\\$/.matcher(doc['winlog.event_data.TargetUserName.keyword'].value);\n    if ( m.matches() ) {\n        return 1;\n    }\n}\nreturn 0;",
                            "lang": "painless"
                        }
                    },
                    "user_logon_only": {
                        "script": {
                            "source": "if (doc.containsKey('winlog.event_data.TargetUserName.keyword') && !doc['winlog.event_data.TargetUserName.keyword'].empty) {\n    if (doc['winlog.event_data.TargetUserName.keyword'].value =~ /^.*\\$$/) {\n        return true;\n    }\n}\nreturn false;",
                            "lang": "painless"
                        }
                    }
                },
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    },
                    {
                        "field": "docker.time",
                        "format": "date_time"
                    },
                    {
                        "field": "event.created",
                        "format": "date_time"
                    },
                    {
                        "field": "nextcloud.time",
                        "format": "date_time"
                    },
                    {
                        "field": "nginx.time_iso8601",
                        "format": "date_time"
                    },
                    {
                        "field": "snoopy.date_iso_8601",
                        "format": "date_time"
                    },
                    {
                        "field": "winlog.event_data.NewTime",
                        "format": "date_time"
                    },
                    {
                        "field": "winlog.event_data.PreviousTime",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "script": {
                                                "script": {
                                                    "source": "boolean compare(Supplier s, def v) {return s.get() == v;}compare(() -> { if (doc.containsKey('winlog.event_data.TargetUserName.keyword') && !doc['winlog.event_data.TargetUserName.keyword'].empty) {\n    if (doc['winlog.event_data.TargetUserName.keyword'].value =~ /^.*\\$$/) {\n        return true;\n    }\n}\nreturn false; }, params.value);",
                                                    "lang": "painless",
                                                    "params": {
                                                        "value": False
                                                    }
                                                }
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "match_phrase": {
                                    "type": "dc"
                                }
                            },
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "match_phrase": {
                                                "winlog.event_id": "4624"
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "winlog.event_id": "4625"
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "winlog.event_id": "4627"
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": date_from,
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
            return body_arms, body
        elif vpo:
            body = {
                "sort": [
                    {
                      "@timestamp": {
                        "order": "desc",
                        "unmapped_type": "boolean"
                      }
                    }
                  ],
                  "aggs": {
                    "2": {
                      "date_histogram": {
                        "field": "@timestamp",
                        "fixed_interval": "12h",
                        "time_zone": "Europe/Moscow",
                        "min_doc_count": 1
                      }
                    }
                  },
                  "stored_fields": [
                    "*"
                  ],
                  "_source": {
                    "excludes": []
                  },
                  "query": {
                    "bool": {
                      "must": [],
                      "filter": [
                        {
                          "bool": {
                            "should": [],
                            "minimum_should_match": 1
                          }
                        },
                        {
                            "exists": {
                                "field": "sd.event.p5"
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": date_from,
                                    "lte": date_to,
                                    "format": "strict_date_optional_time"
                                }
                            }
                        }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
            vpos = open('vpo.txt', 'r').readlines()
            for vpo in vpos:
                vpo = vpo.split('\n')[0]
                body['query']['bool']['filter'][0]['bool']['should'].append({"query_string": {"query": f"*{vpo}*"}})
            if tenant:
                body['query']['bool']['filter'].append({"match_phrase": {"region": tenant}})
            return body
        elif tenant:
            body = {
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "unmapped_type": "boolean"
                        }
                    }
                ],
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "30m",
                            "time_zone": "Europe/Moscow",
                            "min_doc_count": 1
                        }
                    }
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {
                    "region_url": {
                        "script": {
                            "source": "def region_value = doc['region.keyword'].value;",
                            "lang": "painless"
                        }
                    }
                },
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "exists": {
                                    "field": "attack_source_ip"
                                }
                            },
                            {
                                "match_phrase": {
                                    "region": tenant
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        # "gte": "2021-12-26T09:23:24.501Z",
                                        "gte": date_from,
                                        # "lte": "2021-12-27T09:23:24.501Z",
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": [
                            {
                                "match_phrase": {
                                    "attack_source_ip": "0.0.0.0"
                                }
                            },
                            {
                                "match_phrase": {
                                    "attack_target_ip": "0.0.0.0"
                                }
                            }
                        ]
                    }
                }
            }
            return body
        elif stats:
            body = {
                "aggs": {
                    "3": {
                        "cardinality": {
                            "field": "attack_target_ip.keyword"
                        }
                    },
                    "4": {
                        "cardinality": {
                            "field": "attack_source_ip.keyword"
                        }
                    },
                    "6": {
                        "cardinality": {
                            "field": "region.keyword"
                        }
                    }
                },
                "size": 0,
                "stored_fields": [
                    "*"
                ],
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "exists": {
                                    "field": "attack_source_ip"
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": date_from,
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": [
                            {
                                "match_phrase": {
                                    "attack_source_ip.keyword": "0.0.0.0"
                                }
                            },
                            {
                                "match_phrase": {
                                    "attack_target_ip.keyword": "0.0.0.0"
                                }
                            }
                        ]
                    }
                }
            }
            return body
        elif previlege:
            body = {
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "unmapped_type": "boolean"
                        }
                    }
                ],
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "3h",
                            "time_zone": "Europe/Moscow",
                            "min_doc_count": 1
                        }
                    }
                },
                "stored_fields": [
                    "*"
                ],
                "_source": {
                    "excludes": []
                },
                 "query": {
                        "bool": {
                          "must": [],
                          "filter": [
                            {
                              "bool": {
                                "should": [
                                  {
                                    "bool": {
                                      "should": [
                                        {
                                          "query_string": {
                                            "fields": [
                                              "winlog.event_data.TargetUserName"
                                            ],
                                            "query": "*admin*"
                                          }
                                        }
                                      ],
                                      "minimum_should_match": 1
                                    }
                                  },
                                  {
                                    "bool": {
                                      "should": [
                                        {
                                          "bool": {
                                            "should": [
                                              {
                                                "query_string": {
                                                  "fields": [
                                                    "winlog.event_data.TargetUserName"
                                                  ],
                                                  "query": "*админ*"
                                                }
                                              }
                                            ],
                                            "minimum_should_match": 1
                                          }
                                        },
                                        {
                                          "bool": {
                                            "should": [
                                              {
                                                "bool": {
                                                  "should": [
                                                    {
                                                      "query_string": {
                                                        "fields": [
                                                          "winlog.event_data.TargetUserName"
                                                        ],
                                                        "query": "*SupportGroup*"
                                                      }
                                                    }
                                                  ],
                                                  "minimum_should_match": 1
                                                }
                                              },
                                              {
                                                "bool": {
                                                  "should": [
                                                    {
                                                      "bool": {
                                                        "should": [
                                                          {
                                                            "query_string": {
                                                              "fields": [
                                                                "winlog.event_data.TargetUserName"
                                                              ],
                                                              "query": "*AddInDomain*"
                                                            }
                                                          }
                                                        ],
                                                        "minimum_should_match": 1
                                                      }
                                                    },
                                                    {
                                                      "bool": {
                                                        "should": [
                                                          {
                                                            "bool": {
                                                              "should": [
                                                                {
                                                                  "query_string": {
                                                                    "fields": [
                                                                      "winlog.event_data.TargetUserName"
                                                                    ],
                                                                    "query": "*ORA_DBA*"
                                                                  }
                                                                }
                                                              ],
                                                              "minimum_should_match": 1
                                                            }
                                                          },
                                                          {
                                                            "bool": {
                                                              "should": [
                                                                {
                                                                  "bool": {
                                                                    "should": [
                                                                      {
                                                                        "query_string": {
                                                                          "fields": [
                                                                            "winlog.event_data.TargetUserName"
                                                                          ],
                                                                          "query": "*Global Prog*"
                                                                        }
                                                                      }
                                                                    ],
                                                                    "minimum_should_match": 1
                                                                  }
                                                                },
                                                                {
                                                                  "bool": {
                                                                    "should": [
                                                                      {
                                                                        "query_string": {
                                                                          "fields": [
                                                                            "winlog.event_data.TargetUserName"
                                                                          ],
                                                                          "query": "*Organization Management*"
                                                                        }
                                                                      }
                                                                    ],
                                                                    "minimum_should_match": 1
                                                                  }
                                                                }
                                                              ],
                                                              "minimum_should_match": 1
                                                            }
                                                          }
                                                        ],
                                                        "minimum_should_match": 1
                                                      }
                                                    }
                                                  ],
                                                  "minimum_should_match": 1
                                                }
                                              }
                                            ],
                                            "minimum_should_match": 1
                                          }
                                        }
                                      ],
                                      "minimum_should_match": 1
                                    }
                                  }
                                ],
                                "minimum_should_match": 1
                              }
                            },
                            {
                                "match_phrase": {
                                    "type": "dc"
                                }
                            },
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "match_phrase": {
                                                "event.code": "4728"
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "event.code": "4727"
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "event.code": "4729"
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "event.code": "4730"
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": date_from,
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
            return body
        else:
            body = {
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "unmapped_type": "boolean"
                        }
                    }
                ],
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "30m",
                            "time_zone": "Europe/Moscow",
                            "min_doc_count": 1
                        }
                    }
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {
                    "region_url": {
                        "script": {
                            "source": "def region_value = doc['region.keyword'].value;",
                            "lang": "painless"
                        }
                    }
                },
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "exists": {
                                    "field": "attack_source_ip"
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        # "gte": "2021-12-26T09:23:24.501Z",
                                        "gte": date_from,
                                        # "lte": "2021-12-27T09:23:24.501Z",
                                        "lte": date_to,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": [
                            {
                                "match_phrase": {
                                    "attack_source_ip": "0.0.0.0"
                                }
                            },
                            {
                                "match_phrase": {
                                    "attack_target_ip": "0.0.0.0"
                                }
                            }
                        ]
                    }
                }
            }
        return body