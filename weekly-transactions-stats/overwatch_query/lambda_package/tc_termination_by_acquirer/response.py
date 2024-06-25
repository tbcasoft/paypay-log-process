import requests # type: ignore

def get_API_terminate_response(address, start_time, end_time):
    
    headers = {
        'Content-Type': 'application/json',
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

    response = requests.get(f"http://{address}/overwatch-jobmodels-*/_search", 
                            headers=headers, 
                            json=json_data)
                            
    result = response.json()
    return result