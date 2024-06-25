import requests # type: ignore

def get_pairs_response(address, start_time, end_time):


    headers = {
        'Content-Type': 'application/json',
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

    response = requests.get(f"http://{address}/overwatch-jobmodels-*/_search", 
                            headers=headers, 
                            json=json_data)

    result = response.json()
    return result

def get_issuer_currency_response(address, start_time, end_time):

    headers = {
        'Content-Type': 'application/json',
    }


    json_data = {
        'aggs': {
            '2': {
                'terms': {
                    'field': 'type.keyword',
                    'order': {
                        '1': 'desc',
                    },
                    'size': 5,
                },
                'aggs': {
                    '1': {
                        'sum': {
                            'field': 'merchantRefundRequest.amount',
                        },
                    },
                    '8': {
                        'terms': {
                            'field': 'tbca_metadata.env.siteSrc.keyword',
                            'order': {
                                '_key': 'asc',
                            },
                            'size': 5,
                        },
                        'aggs': {
                            '3': {
                                'terms': {
                                    'field': 'status.keyword',
                                    'order': {
                                        '1': 'desc',
                                    },
                                    'size': 5,
                                },
                                'aggs': {
                                    '1': {
                                        'sum': {
                                            'field': 'merchantRefundRequest.amount',
                                        },
                                    },
                                    '4': {
                                        'terms': {
                                            'field': 'merchantRefundRequest.fromIssuer.keyword',
                                            'order': {
                                                '1': 'desc',
                                            },
                                            'size': 5,
                                        },
                                        'aggs': {
                                            '1': {
                                                'sum': {
                                                    'field': 'merchantRefundRequest.amount',
                                                },
                                            },
                                            '7': {
                                                'terms': {
                                                    'field': 'merchantRefundRequest.currency.keyword',
                                                    'order': {
                                                        '_count': 'desc',
                                                    },
                                                    'size': 5,
                                                },
                                                'aggs': {
                                                    '5': {
                                                        'terms': {
                                                            'field': 'merchantRefundRequest.toIssuer.keyword',
                                                            'order': {
                                                                '1': 'desc',
                                                            },
                                                            'size': 5,
                                                        },
                                                        'aggs': {
                                                            '1': {
                                                                'sum': {
                                                                    'field': 'merchantRefundRequest.amount',
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
                            'type.keyword': 'MS_REFUND',
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