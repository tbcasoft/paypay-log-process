from collections import defaultdict
import json
from response import get_job_models_invoice_response
import ultraimport # type: ignore

get_time = ultraimport('__dir__/../generate_time.py', 'get_time')
tc_login = ultraimport('__dir__/../tc_login.py')

start_time, end_time = get_time()

test_cookie = tc_login.get_test_cookie()

job_modles_invoice_response = get_job_models_invoice_response(test_cookie, start_time, end_time)

def process_job_modles_invoice_response(response):

    # print(json.dumps(response, indent=4))
    data_collector = defaultdict(dict)
    sub_dict = response["aggregations"]["0"]["buckets"]

    for src in sub_dict:
        count = src["1"]["buckets"][1]["doc_count"]
        data_collector[src["key"]] = {
            "rejected_count": count
        }
        
    return data_collector

job_modles_invoice_data = process_job_modles_invoice_response(job_modles_invoice_response)
print(json.dumps(job_modles_invoice_data, indent=4))
