from collections import defaultdict
from .response import get_API_gen_target_response

def process_gen_target_response(response):
    
    
    data_collector = defaultdict(dict)
    sub_dict = response["aggregations"]["0"]["buckets"][0]["1"]["buckets"]

    for site_src in sub_dict:
        data_collector[site_src["key"]] = {
            "count": site_src["doc_count"]
        }
        
    return data_collector

def get_dashboard_data(address, start_time, end_time, issuers):

    gen_target_response = get_API_gen_target_response(address, start_time, end_time)

    gen_target_data = process_gen_target_response(gen_target_response)

    checkDefault(gen_target_data, issuers)

    return gen_target_data

def checkDefault(data, issuers):
    for issuer in issuers:
        if issuer not in data:
            data[issuer] = {
                "count": 0
            }
