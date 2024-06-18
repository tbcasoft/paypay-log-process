from collections import defaultdict
import json
from .response import get_API_gen_target_response

def process_gen_target_response(response):

    # print(json.dumps(response, indent=4))
    data_collector = defaultdict(dict)
    sub_dict = response["aggregations"]["0"]["buckets"][0]["1"]["buckets"]

    for site_src in sub_dict:
        data_collector[site_src["key"]] = {
            "count": site_src["doc_count"]
        }
        
    return data_collector

def get_dashboard_data(cookie, start_time, end_time):

    gen_target_response = get_API_gen_target_response(cookie, start_time, end_time)

    gen_target_data = process_gen_target_response(gen_target_response)

    print(json.dumps(gen_target_data, indent=4))

    return gen_target_data

