# import os, sys
# sys.path.append(os.path.dirname(__file__))
from collections import defaultdict
import json
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

def get_dashboard_data(cookie, start_time, end_time):   

    jobmodels_RFP_response = get_jobmodels_RFP_response(cookie, start_time, end_time)

    jobmodels_RFP_data = process_jobmodels_RFP_response(jobmodels_RFP_response)

    # print(json.dumps(jobmodels_RFP_data, indent=4))

    return jobmodels_RFP_data
