from .response import get_technical_jobmodels_response

def process_technical_jobmodels_response(response):

    hivex_network_peak_request = response["aggregations"]["0"]["buckets"][0]["1"]["buckets"][0]["2"]["value"]
        
    return hivex_network_peak_request

def get_dashboard_data(address, start_time, end_time):   

    technical_jobmodels_response = get_technical_jobmodels_response(address, start_time, end_time)

    hivex_network_peak_request = process_technical_jobmodels_response(technical_jobmodels_response)

    return hivex_network_peak_request