import json
import ultraimport # type: ignore
import requests # type: ignore

get_time = ultraimport('__dir__/../generate_time.py', 'get_time')

def get_job_models_invoice_response(cookie, start_time, end_time):

    cookies = {
        'tcSession': cookie,
    }

    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'tcSession=MTcxODU5NTQwM3xHd3dBR0RZMk5tWmhNREl4TUdNd01XUmpZV0l3T1RrNU5UQTNZZz09fK3viv76P_Si2R4XaMHTs0nKsNxo0tcdb4LFNspRClrS',
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
            '0': {
                'terms': {
                    'field': 'sourceTelcoId.keyword',
                    'order': {
                        '_count': 'desc',
                    },
                    'size': 10,
                },
                'aggs': {
                    '1': {
                        'terms': {
                            'field': 'status.keyword',
                            'order': {
                                '_count': 'desc',
                            },
                            'size': 5,
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
                                        'tbca_metadata.env.siteSrc.keyword': 'ESB',
                                    },
                                },
                                {
                                    'match_phrase': {
                                        'tbca_metadata.env.siteSrc.keyword': 'JKO',
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
                            'type.keyword': 'U_INVOICE',
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
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    result = response.json()
    return result
