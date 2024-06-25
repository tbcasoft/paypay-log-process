from collections import defaultdict
from .response import get_job_models_invoice_response

def process_job_modles_invoice_response(response):

    data_collector = defaultdict(dict)
    sub_dict = response["aggregations"]["0"]["buckets"]

    for src in sub_dict:
        count = src["1"]["buckets"][1]["doc_count"]
        data_collector[src["key"]] = {
            "rejected_count": count
        }
        
    return data_collector

def get_dashboard_data(address, start_time, end_time, issuers):

    job_modles_invoice_response = get_job_models_invoice_response(address, start_time, end_time)

    job_modles_invoice_data = process_job_modles_invoice_response(job_modles_invoice_response)

    checkDefault(job_modles_invoice_data, issuers)

    return job_modles_invoice_data

def checkDefault(data, issuers):
    for issuer in issuers:
        if issuer not in data:
            data[issuer] = {
                "rejected_count": 0
            }