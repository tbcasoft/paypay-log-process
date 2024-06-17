import json
import ultraimport # type: ignore
import requests # type: ignore

get_time = ultraimport('__dir__/../generate_time.py', 'get_time')

# start_time, end_time = getTime()
start_time, end_time = "2024-06-14T06:45:00.000Z", "2024-06-14T07:00:00.000Z"

def get_response(cookie, start_time, end_time):

    cookies = {
        # 'tcSession': cookie,
        'tcSession': 'MTcxODU5NTQwM3xHd3dBR0RZMk5tWmhNREl4TUdNd01XUmpZV0l3T1RrNU5UQTNZZz09fK3viv76P_Si2R4XaMHTs0nKsNxo0tcdb4LFNspRClrS',
    }

    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'tcSession=MTcxODU5MTUyNnxHd3dBR0RZMk5tWmhNREl4TUdNd01XUmpZV0l3T1RrNU5UQTNZZz09fAVkQoLgHmYmTBb4f9qH1gxmA8pbBhvornFBm5X3tgy-',
        'Origin': 'https://tc-2pn1ygvtl5.xiveh.com',
        'Referer': 'https://tc-2pn1ygvtl5.xiveh.com/kibana/s/node-operator/app/dev_tools',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'kbn-xsrf': 'kibana',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'path': 'overwatch-jobmodels-*/_search',
        'method': 'GET',
    }

    json_data = {
        'aggs': {
            '7': {
                'terms': {
                    'field': 'type.keyword',
                    'order': {
                        '_key': 'desc',
                    },
                    'size': 5,
                },
                'aggs': {
                    '13': {
                        'terms': {
                            'field': 'paymentFlow.keyword',
                            'order': {
                                '_count': 'desc',
                            },
                            'size': 3,
                        },
                        'aggs': {
                            '8': {
                                'terms': {
                                    'field': 'status.keyword',
                                    'order': {
                                        '_key': 'desc',
                                    },
                                    'size': 5,
                                },
                                'aggs': {
                                    '9': {
                                        'terms': {
                                            'field': 'tbca_metadata.env.siteSrc.keyword',
                                            'order': {
                                                '_key': 'desc',
                                            },
                                            'size': 5,
                                        },
                                        'aggs': {
                                            '5': {
                                                'terms': {
                                                    'field': 'merchantPaymentRequest.fromIssuer.keyword',
                                                    'order': {
                                                        '_key': 'desc',
                                                    },
                                                    'size': 5,
                                                },
                                                'aggs': {
                                                    '12': {
                                                        'terms': {
                                                            'field': 'fundingCurrency.keyword',
                                                            'order': {
                                                                '_count': 'desc',
                                                            },
                                                            'size': 5,
                                                        },
                                                        'aggs': {
                                                            '6': {
                                                                'terms': {
                                                                    'field': 'merchantPaymentRequest.toIssuer.keyword',
                                                                    'order': {
                                                                        '_key': 'desc',
                                                                    },
                                                                    'size': 5,
                                                                },
                                                                'aggs': {
                                                                    '4': {
                                                                        'terms': {
                                                                            'field': 'finalAmounts.destCurrency.keyword',
                                                                            'order': {
                                                                                '_key': 'desc',
                                                                            },
                                                                            'size': 5,
                                                                        },
                                                                        'aggs': {
                                                                            '3': {
                                                                                'sum': {
                                                                                    'field': 'finalAmounts.destAmount',
                                                                                },
                                                                            },
                                                                            '11': {
                                                                                'sum': {
                                                                                    'field': 'fundingAmount',
                                                                                },
                                                                            },
                                                                        },
                                                                    },
                                                                },
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        'size': 0,
        'fields': [
            {
                'field': '@timestamp',
                'format': 'date_time',
            },
        ],
        'script_fields': {},
        'stored_fields': [
            '*',
        ],
        'runtime_mappings': {},
        '_source': {
            'excludes': [],
        },
        'query': {
            'bool': {
                'must': [],
                'filter': [
                    {
                        'bool': {
                            'should': [
                                {
                                    'match_phrase': {
                                        'tbca_metadata.env.siteSrc.keyword': 'JKO',
                                    },
                                },
                                {
                                    'match_phrase': {
                                        'tbca_metadata.env.siteSrc.keyword': 'ESB',
                                    },
                                },
                                {
                                    'match_phrase': {
                                        'tbca_metadata.env.siteSrc.keyword': 'PXP',
                                    },
                                },
                            ],
                            'minimum_should_match': 1,
                        },
                    },
                    {
                        'match_phrase': {
                            'type.keyword': 'U_PAY',
                        },
                    },
                    {
                        'range': {
                            '@timestamp': {
                                'format': 'strict_date_optional_time',
                                'gte': start_time,
                                'lte': end_time,
                            },
                        },
                    },
                ],
                'should': [],
                'must_not': [],
            },
        },
    }

    response = requests.post(
        'https://tc-2pn1ygvtl5.xiveh.com/kibana/s/node-operator/api/console/proxy',
        params=params,
        # cookies=cookies,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n  "aggs": {\n    "7": {\n      "terms": {\n        "field": "type.keyword",\n        "order": {\n          "_key": "desc"\n        },\n        "size": 5\n      },\n      "aggs": {\n        "13": {\n          "terms": {\n            "field": "paymentFlow.keyword",\n            "order": {\n              "_count": "desc"\n            },\n            "size": 3\n          },\n          "aggs": {\n            "8": {\n              "terms": {\n                "field": "status.keyword",\n                "order": {\n                  "_key": "desc"\n                },\n                "size": 5\n              },\n              "aggs": {\n                "9": {\n                  "terms": {\n                    "field": "tbca_metadata.env.siteSrc.keyword",\n                    "order": {\n                      "_key": "desc"\n                    },\n                    "size": 5\n                  },\n                  "aggs": {\n                    "5": {\n                      "terms": {\n                        "field": "merchantPaymentRequest.fromIssuer.keyword",\n                        "order": {\n                          "_key": "desc"\n                        },\n                        "size": 5\n                      },\n                      "aggs": {\n                        "12": {\n                          "terms": {\n                            "field": "fundingCurrency.keyword",\n                            "order": {\n                              "_count": "desc"\n                            },\n                            "size": 5\n                          },\n                          "aggs": {\n                            "6": {\n                              "terms": {\n                                "field": "merchantPaymentRequest.toIssuer.keyword",\n                                "order": {\n                                  "_key": "desc"\n                                },\n                                "size": 5\n                              },\n                              "aggs": {\n                                "4": {\n                                  "terms": {\n                                    "field": "finalAmounts.destCurrency.keyword",\n                                    "order": {\n                                      "_key": "desc"\n                                    },\n                                    "size": 5\n                                  },\n                                  "aggs": {\n                                    "3": {\n                                      "sum": {\n                                        "field": "finalAmounts.destAmount"\n                                      }\n                                    },\n                                    "11": {\n                                      "sum": {\n                                        "field": "fundingAmount"\n                                      }\n                                    }\n                                  }\n                                }\n                              }\n                            }\n                          }\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  },\n  "size": 0,\n  "fields": [\n    {\n      "field": "@timestamp",\n      "format": "date_time"\n    }\n  ],\n  "script_fields": {},\n  "stored_fields": [\n    "*"\n  ],\n  "runtime_mappings": {},\n  "_source": {\n    "excludes": []\n  },\n  "query": {\n    "bool": {\n      "must": [],\n      "filter": [\n        {\n          "bool": {\n            "should": [\n              {\n                "match_phrase": {\n                  "tbca_metadata.env.siteSrc.keyword": "JKO"\n                }\n              },\n              {\n                "match_phrase": {\n                  "tbca_metadata.env.siteSrc.keyword": "ESB"\n                }\n              },\n              {\n                "match_phrase": {\n                  "tbca_metadata.env.siteSrc.keyword": "PXP"\n                }\n              }\n            ],\n            "minimum_should_match": 1\n          }\n        },\n        {\n          "match_phrase": {\n            "type.keyword": "U_PAY"\n          }\n        },\n        {\n          "range": {\n            "@timestamp": {\n              "format": "strict_date_optional_time",\n              "gte": "2024-06-17T02:18:26.640Z",\n              "lte": "2024-06-17T02:33:26.640Z"\n            }\n          }\n        }\n      ],\n      "should": [],\n      "must_not": []\n    }\n  }\n}\n'
#response = requests.post(
#    'https://tc-2pn1ygvtl5.xiveh.com/kibana/s/node-operator/api/console/proxy',
#    params=params,
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)

    result = response.json()
    return result

