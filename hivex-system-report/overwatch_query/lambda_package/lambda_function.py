import json
import os
import pymysql
from generate_time import get_time
from update_db import update_issuers_table, update_weekly_stats_table

from technical_dashboard import process as technical_d
from issuer_dashboard import process as issuer_d
from dynamodb import dynamodb_query

def lambda_handler(event, context):
    
    db_connection = pymysql.connect(
        host=os.environ["db_host"],
        port=int(os.environ["db_port"]),
        database=os.environ["db_name"],
        user=os.environ["db_username"],
        password=os.environ["db_password"]
    )

    address = os.environ["requests_address"]

    start_time, end_time = get_time()
    issuers = ["JKO", "ESB", "PXP"]
    acquiers = ["PPY"]
    
    hivex_network_peak_request = technical_d.get_dashboard_data(address, start_time, end_time)
    get_invoice_latency_data, pay_latency_data, conf_page_latency_data = issuer_d.get_dashboard_data(address, start_time, end_time, issuers)
    num_onboarded_merchant_services = dynamodb_query.query_db()
    

    
    response_data = {
        'weekly_stats': {
            'hivex_network_peak_request': hivex_network_peak_request,
            'num_onboarded_merchant_services': num_onboarded_merchant_services
        },
        'get_invoice_latency_data': get_invoice_latency_data,
        'pay_latency_data': pay_latency_data,
        'conf_page_latency_data': conf_page_latency_data
    }
    
    update_issuers_table(db_connection, start_time, response_data, issuers, acquiers)
    update_weekly_stats_table(db_connection, start_time, response_data)
    db_connection.close()
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }