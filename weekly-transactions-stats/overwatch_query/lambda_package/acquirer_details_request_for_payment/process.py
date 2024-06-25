from collections import defaultdict
from .response import get_jobmodels_RFP_response

def process_jobmodels_RFP_response(response):
    
    data_collector = defaultdict(dict)
    # print(json.dumps(response, indent=4))

    rejected = response["aggregations"]["0"]["buckets"][1]["1"]["buckets"]

    for target_carrier_id in rejected:
        data_collector[target_carrier_id["key"]] = {
            "rejected_count": target_carrier_id["2"]["value"]
        }
        
    return data_collector

def get_dashboard_data(address, start_time, end_time, issuers):   

    jobmodels_RFP_response = get_jobmodels_RFP_response(address, start_time, end_time)

    jobmodels_RFP_data = process_jobmodels_RFP_response(jobmodels_RFP_response)

    checkDefault(jobmodels_RFP_data, issuers)

    return jobmodels_RFP_data

def checkDefault(data, issuers):
    for issuer in issuers:
        if issuer not in data:
            data[issuer] = {
                "rejected_count": 0
            }