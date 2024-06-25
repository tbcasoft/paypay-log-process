import requests # type: ignore

def get_job_models_invoice_response(address, start_time, end_time):

    headers = {
        'Content-Type': 'application/json',
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
    
    response = requests.get(f"http://{address}/overwatch-jobmodels-*/_search", 
                            headers=headers, 
                            json=json_data)

    result = response.json()
    return result