from collections import defaultdict
from .response import get_issuer_currency_response, get_pairs_response

def process_pair_response(response):

    data_collector = {
    "CPM" : defaultdict(dict),
    "MPM" : defaultdict(dict)
    }

    cpm_data = data_collector["CPM"]
    mpm_data = data_collector["MPM"]
    
    buckets = response["aggregations"]["7"]["buckets"][0]

    cpm_payment_flow = buckets["13"]["buckets"][0]["8"]["buckets"][0]["9"]["buckets"]
    mpm_payment_flow = buckets["13"]["buckets"][1]["8"]["buckets"][0]["9"]["buckets"]


    def get_data(payment_flow , data_dict):
        for issuer_dict in payment_flow:
            from_issuer = issuer_dict["key"]
            sub_dict = issuer_dict["5"]["buckets"][0]["12"]["buckets"][0]["6"]["buckets"][0]["4"]["buckets"][0]
            issuer = data_dict[from_issuer]
            issuer["count"] = sub_dict["doc_count"]
            issuer["dest_amount"] = sub_dict["3"]["value"]  

    get_data(cpm_payment_flow, cpm_data)
    get_data(mpm_payment_flow, mpm_data)

    return data_collector

def process_issuer_currency_response(response):

    data_collector = defaultdict(dict)

    toIssuers_lst = response["aggregations"]["2"]["buckets"][0]["8"]["buckets"]

    for issuer_dict in toIssuers_lst:
        issuer = issuer_dict["key"]
        issuer = data_collector[issuer_dict["key"]]
        issuer["count"] = issuer_dict["doc_count"]

        sum_of_amount = issuer_dict["3"]["buckets"][0]["1"]["value"]
        issuer["sum_of_amount"] = sum_of_amount
    
    return data_collector
        

def get_dashboard_data(address, start_time, end_time, issuers):

    pairs_response = get_pairs_response(address, start_time, end_time)
    issuer_currency_response = get_issuer_currency_response(address, start_time, end_time)

    issuer_currency_data = process_issuer_currency_response(issuer_currency_response)
    pairs_data = process_pair_response(pairs_response)

    checkDefault(issuer_currency_data, pairs_data, issuers)

    return issuer_currency_data, pairs_data

def checkDefault(refunds_data, payment_flow_data, issuers):
    for issuer in issuers:
        if issuer not in refunds_data:
            refunds_data[issuer] = {
                "count": 0,
                "sum_of_amount": 0
            }
        if issuer not in payment_flow_data["CPM"]:
            payment_flow_data["CPM"][issuer] = {
                "count": 0,
                "dest_amount": 0
            }
        if issuer not in payment_flow_data["MPM"]:
            payment_flow_data["MPM"][issuer] = {
                "count": 0,
                "dest_amount": 0
            } 