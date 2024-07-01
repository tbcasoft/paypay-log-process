import requests # type: ignore


def get_get_invoice_latency_response(address, start_time, end_time, num_issuers):

    headers = {
        'Content-Type': 'application/json',
    }
    
    json_data = {
                  "aggs": {
                    "siteSrc_stats": {  
                      "terms": {
                        "field": "tbca_metadata.env.siteSrc.keyword",
                        "size": num_issuers
                      },
                      "aggs": {
                        "latency": {
                          "percentiles": {
                            "field": "apiElapsedTime",
                            "percents": [50, 99]
                          }
                        }
                      }
                    }
                  },
                  "size": 0,
                  "query": {
                    "bool": {
                      "filter": [
                        {
                          "bool": {
                            "should": [
                              { "match_phrase": { "tbca_metadata.env.siteSrc.keyword": "ESB" } },
                              { "match_phrase": { "tbca_metadata.env.siteSrc.keyword": "JKO" } },
                              { "match_phrase": { "tbca_metadata.env.siteSrc.keyword": "PXP" } }
                            ],
                            "minimum_should_match": 1
                          }
                        },
                        { "match_phrase": { "name.keyword": "INVOICING" } },
                        { "match_phrase": { "eventType.keyword": "SLO" } },
                        {
                          "range": {
                            "@timestamp": {
                              "gte": start_time,
                              "lte": end_time,
                              "format": "strict_date_optional_time"
                            }
                          }
                        }
                      ]
                    }
                  }
                }
    
    response = requests.get(f"http://{address}/overwatch-core-*/_search", 
                            headers=headers, 
                            json=json_data)
    
    result = response.json()
    return result
    

def get_pay_latency_response(address, start_time, end_time, num_issuers):

    headers = {
        'Content-Type': 'application/json',
    }
    
    json_data = {
                  "aggs":{
                    "siteSrc_stats": {
                      "terms": {
                        "field": "tbca_metadata.env.siteSrc.keyword",
                        "size": num_issuers
                      },
                      "aggs": {
                        "latency": {
                          "percentiles": {
                            "field": "elapsedTime",
                            "percents": [50, 99]
                          }
                        }
                      }
                    }
                  },
                  "size": 0,
                  "fields": [
                    {
                      "field": "@timestamp",
                      "format": "date_time"
                    }
                  ],
                  "script_fields": {},
                  "stored_fields": [
                    "*"
                  ],
                  "runtime_mappings": {},
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
                              {"match_phrase": {"tbca_metadata.env.siteSrc.keyword": "ESB"}},
                              {"match_phrase": {"tbca_metadata.env.siteSrc.keyword": "JKO"}},
                              {"match_phrase": {"tbca_metadata.env.siteSrc.keyword": "PXP"}}
                              ], 
                              "minimum_should_match": 1
                          }
                        },
                        {
                          "match_phrase": {
                            "name.keyword": "U_PAY"
                          }
                        },
                        {
                          "match_phrase": {
                            "eventType.keyword": "JOB_TERMINAL"
                          }
                        },
                        {
                          "range": {
                            "@timestamp": {
                              "format": "strict_date_optional_time",
                              "gte": start_time,
                              "lte": end_time
                            }
                          }
                        }
                      ],
                      "should": [],
                      "must_not": []
                    }
                  }
                }
    
    response = requests.get(f"http://{address}/overwatch-core-*/_search", 
                            headers=headers, 
                            json=json_data)
    
    result = response.json()
    return result
  

def get_conf_page_latency_response(address, start_time, end_time, num_issuers):

    headers = {
        'Content-Type': 'application/json',
    }
    
    json_data = {
                  "aggs":{
                    "siteSrc_stats": {
                      "terms": {
                        "field": "tbca_metadata.env.siteSrc.keyword",
                        "size": num_issuers
                      },
                      "aggs": {
                        "latency": {
                          "percentiles": {
                            "field": "elapsedMs",
                            "percents": [
                              50, 99
                            ]
                          }
                        }
                      }
                    }
                  },
                  "size": 0,
                  "fields": [
                    {
                      "field": "@timestamp",
                      "format": "date_time"
                    }
                  ],
                  "script_fields": {},
                  "stored_fields": [
                    "*"
                  ],
                  "runtime_mappings": {},
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
                                "match_phrase": {
                                  "tbca_metadata.env.siteSrc.keyword": "JKO"
                                }
                              },
                              {
                                "match_phrase": {
                                  "tbca_metadata.env.siteSrc.keyword": "ESB"
                                }
                              },
                              {
                                "match_phrase": {
                                  "tbca_metadata.env.siteSrc.keyword": "PXP"
                                }
                              }
                            ],
                            "minimum_should_match": 1
                          }
                        },
                        {
                          "match_phrase": {
                            "path.keyword": "/capi/views/final.html"
                          }
                        },
                        {
                          "range": {
                            "@timestamp": {
                              "format": "strict_date_optional_time",
                              "gte": start_time,
                              "lte": end_time
                            }
                          }
                        }
                      ],
                      "should": [],
                      "must_not": []
                    }
                  }
                }


    response = requests.get(f"http://{address}/overwatch-core-*/_search", 
                            headers=headers, 
                            json=json_data)
    
    result = response.json()
    return result