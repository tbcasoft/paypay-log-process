from collections import defaultdict
import json
from response import *
import ultraimport # type: ignore

get_time = ultraimport('__dir__/../generate_time.py', 'get_time')
tc_login = ultraimport('__dir__/../tc_login.py')

start_time, end_time = get_time()

test_cookie = tc_login.get_test_cookie()

jobmodels_RFP_response = get_jobmodels_RFP_response(test_cookie, start_time, end_time)

def process_jobmodels_RFP_response(response):
    
    data_collector = defaultdict(dict)
    # print(json.dumps(response, indent=4))

    rejected = response["aggregations"]["0"]["buckets"][1]["1"]["buckets"]

    for target_carrier_id in rejected:
        data_collector[target_carrier_id["key"]] = {
            "count": target_carrier_id["2"]["value"]
        }
        
    return data_collector

jobmodels_RFP_data = process_jobmodels_RFP_response(jobmodels_RFP_response)
print(json.dumps(jobmodels_RFP_data, indent=4))
