from collections import defaultdict
import json
from .response import get_API_terminate_response

def process_api_terminate_response(response):

    # print(json.dumps(response, indent=4))
    data_collector = defaultdict(dict)
    sub_dict = response["aggregations"]["0"]["buckets"]
    rejectCodes = [(code["key"], code["1"]["buckets"]) for code in sub_dict]

    for rejectCode_dict in rejectCodes:
        rejectCode = data_collector[rejectCode_dict[0]]
        for issuer in rejectCode_dict[1]:
            rejectCode[issuer["key"]] = issuer["doc_count"]
        

    return data_collector

def get_dashboard_data(cookie, start_time, end_time, issuers):

    api_terminate_response = get_API_terminate_response(cookie, start_time, end_time)

    api_terminate_data = process_api_terminate_response(api_terminate_response)

    checkDefault(api_terminate_data, issuers)

    # print(json.dumps(api_terminate_data, indent=4))

    return api_terminate_data

def checkDefault(data, issuers):
    for rejectCode in data.values():
        for issuer in issuers:
            if issuer not in rejectCode:
                rejectCode[issuer] = 0
            



