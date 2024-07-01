from collections import defaultdict
from .response import get_get_invoice_latency_response, get_pay_latency_response, get_conf_page_latency_response
import json


def process_response(response):
    
    data_collector = defaultdict(dict)

    # print(json.dumps(response, indent=4))

    site_sources = response["aggregations"]["siteSrc_stats"]["buckets"]
    
    for site_src in site_sources:
        data_collector[site_src["key"]] = {
            "median": site_src["latency"]["values"]["50.0"],
            "p99": site_src["latency"]["values"]["99.0"]
        }
        
    # print(json.dumps(data_collector, indent=4))
    return data_collector

def get_dashboard_data(address, start_time, end_time, issuers):   

    num_issuers = len(issuers)
    
    get_invoice_latency_response = get_get_invoice_latency_response(address, start_time, end_time, num_issuers)
    pay_latency_response = get_pay_latency_response(address, start_time, end_time, num_issuers)
    conf_page_latency_response = get_conf_page_latency_response(address, start_time, end_time, num_issuers)

    get_invoice_latency_data = process_response(get_invoice_latency_response)
    pay_latency_data = process_response(pay_latency_response)
    conf_page_latency_data = process_response(conf_page_latency_response)
    
    checkDefault(issuers, get_invoice_latency_data, pay_latency_data, conf_page_latency_data)

    return get_invoice_latency_data, pay_latency_data, conf_page_latency_data

def checkDefault(issuers, get_invoice_latency_data, pay_latency_data, conf_page_latency_data):
    for issuer in issuers:
        if issuer not in get_invoice_latency_data:
            get_invoice_latency_data[issuer] = {
                "median": 0.0,
                "p99": 0.0
            }
        if issuer not in pay_latency_data:
            pay_latency_data[issuer] = {
                "median": 0.0,
                "p99": 0.0
            }
        if issuer not in conf_page_latency_data:
            conf_page_latency_data[issuer] = {
                "median": 0.0,
                "p99": 0.0
            }