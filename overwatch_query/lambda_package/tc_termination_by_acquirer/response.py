import requests # type: ignore

def get_API_terminate_response(cookie, start_time, end_time):
    print("response was called")
    cookies = {
        'tcSession': cookie,
    }

    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'tcSession=MTcxODkzMjkyM3xHd3dBR0RZMk56UmtOV0kyTUdNd01XUmpZV0l3T1RrNU5UQmlaZz09fC6OVx0AJhOUjeVLy0PBc6aw8G1PakhtbyzECfZs8saO',
        'Origin': 'https://tc-2pn1ygvtl5.xiveh.com',
        'Referer': 'https://tc-2pn1ygvtl5.xiveh.com/kibana/s/tbca-central/app/dev_tools',
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
                    'field': 'rejectCode.keyword',
                    'order': {
                        '_key': 'desc',
                    },
                    'size': 3,
                },
                'aggs': {
                    '1': {
                        'terms': {
                            'field': 'tbca_metadata.env.siteSrc.keyword',
                            'order': {
                                '_key': 'asc',
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
                        'match_phrase': {
                            'type': 'MS_TERMINATE_FLOW',
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
                'must_not': [
                    {
                        'match_phrase': {
                            'tbca_metadata.env.siteSrc': 'PPY',
                        },
                    },
                ],
            },
        },
    }

    response = requests.post(
        'https://tc-2pn1ygvtl5.xiveh.com/kibana/s/tbca-central/api/console/proxy',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    result = response.json()
    return result
