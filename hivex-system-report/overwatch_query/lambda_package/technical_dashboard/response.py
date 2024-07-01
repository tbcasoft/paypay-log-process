import requests # type: ignore
import json

def get_technical_jobmodels_response(address, start_time, end_time):

    headers = {
        'Content-Type': 'application/json',
    }
    
    json_data = {
                  "aggs": {
                    "0": {
                      "terms": {
                        "field": "ledgerSequence",
                        "order": {
                          "2": "desc"
                        },
                        "size": 1
                      },
                      "aggs": {
                        "1": {
                          "date_histogram": {
                            "field": "@timestamp",
                            "calendar_interval": "1h",
                            "time_zone": "UTC"
                          },
                          "aggs": {
                            "2": {
                              "cardinality": {
                                "field": "jobId.keyword"
                              }
                            }
                          }
                        },
                        "2": {
                          "cardinality": {
                            "field": "jobId.keyword"
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
    
    response = requests.get(f"http://{address}/overwatch-jobmodels-*/_search", 
                            headers=headers, 
                            json=json_data)
    
    result = response.json()
    return result