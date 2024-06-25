import requests # type: ignore
import json

def get_jobmodels_RFP_response(address, start_time, end_time):

    headers = {
        'Content-Type': 'application/json',
    }
    
    json_data = {
        'aggs': {
            '0': {
                'terms': {
                    'field': 'status.keyword',
                    'order': {
                        '2': 'desc',
                    },
                    'size': 10,
                },
                'aggs': {
                    '1': {
                        'terms': {
                            'field': 'targetCarrierId.keyword',
                            'order': {
                                '2': 'desc',
                            },
                            'size': 10,
                        },
                        'aggs': {
                            '2': {
                                'cardinality': {
                                    'field': 'jobId.keyword',
                                },
                            },
                        },
                    },
                    '2': {
                        'cardinality': {
                            'field': 'jobId.keyword',
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
                                        'tbca_metadata.env.siteSrc.keyword': 'PPY',
                                    },
                                },
                            ],
                            'minimum_should_match': 1,
                        },
                    },
                    {
                        'match_phrase': {
                            'type.keyword': 'MS_REQUEST_FOR_PAYMENT',
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
    # print(json.dumps(result, indent=4))
    return result
    
    