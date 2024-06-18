from collections import defaultdict
import json
from .response import get_job_models_invoice_response

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

def get_dashboard_data(cookie, start_time, end_time):

    job_modles_invoice_response = get_job_models_invoice_response(cookie, start_time, end_time)

    job_modles_invoice_data = process_job_modles_invoice_response(job_modles_invoice_response)

    print(json.dumps(job_modles_invoice_data, indent=4))

    return job_modles_invoice_data
