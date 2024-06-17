from collections import defaultdict
import json
from response import *
import ultraimport # type: ignore

get_time = ultraimport('__dir__/../generate_time.py', 'get_time')
tc_login = ultraimport('__dir__/../tc_login.py')

start_time, end_time = get_time()

test_cookie = tc_login.get_test_cookie()

gen_target_response = get_API_gen_target_response(test_cookie, start_time, end_time)

def process_gen_target_response(response):

    # print(json.dumps(response, indent=4))
    data_collector = defaultdict(dict)
    sub_dict = response["aggregations"]["0"]["buckets"][0]["1"]["buckets"]

    for site_src in sub_dict:
        data_collector[site_src["key"]] = {
            "count": site_src["doc_count"]
        }
        
    return data_collector

gen_target_data = process_gen_target_response(gen_target_response)
print(json.dumps(gen_target_data, indent=4))
