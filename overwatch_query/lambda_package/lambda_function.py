import json
import pymysql
from generate_time import get_time
import issuer_details_target_generation.process
from tc_login import get_test_cookie
from acquirer_details_request_for_payment import process as req_for_payment 
from buisness_dashboard import process as buisness
from issuer_details_get_invoice import process as get_invoice
from issuer_details_target_generation import process as target_gen


def lambda_handler(event, context):
    db_connection = pymysql.connect(
        host='visa-fx-05006aa44b45542b.elb.ap-southeast-1.amazonaws.com',
        port=1234,
        database='hour_qr',
        user='aws_lambda',
        password='&o17r%FK$Ft8'
    )
    start_time, end_time = get_time()
    test_cookie = get_test_cookie()

    rejected_job_models_invoice_data = get_invoice.get_dashboard_data(test_cookie, start_time, end_time)

    rejected_job_models_RFP_data = req_for_payment.get_dashboard_data(test_cookie, start_time, end_time)
    
    api_gen_target_data = target_gen.get_dashboard_data(test_cookie, start_time, end_time)
    
    payment_flows_data, refunds_data = buisness.get_dashboard_data(test_cookie, start_time, end_time)
    
    # print(json.dumps(payment_flows_data, indent=4))
    
    # mainnet_update_db.update_analysis_table(connection=db_connection, start_time=s, log_event_streams=event_streams)
    # mainnet_update_db.update_raw_table(connection=db_connection, log_event_streams=event_streams)

    db_connection.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps("success!!")
    }

lambda_handler(1,1)