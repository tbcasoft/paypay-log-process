import json
import pymysql
from generate_time import get_time
from tc_login import get_test_cookie
from acquirer_details_request_for_payment import process as req_for_payment 
from buisness_dashboard import process as buisness
from issuer_details_get_invoice import process as get_invoice
from issuer_details_target_generation import process as target_gen
from tc_termination_by_acquirer import process as api_terminate
from update_db import update_dashboard_table


def lambda_handler(event, context):
    db_connection = pymysql.connect(
        host='visa-fx-05006aa44b45542b.elb.ap-southeast-1.amazonaws.com',
        port=1234,
        database='hour_qr',
        user='aws_lambda',
        password='&o17r%FK$Ft8'
    )

    start_time, end_time = get_time()
    # start_time, end_time = "2024-06-19T00:00:00.000Z", "2024-06-20T00:00:00.000Z"
    test_cookie = get_test_cookie()
    ISSUERS = ["JKO", "ESB", "PXP"]

    rejected_job_models_invoice_data = get_invoice.get_dashboard_data(test_cookie, start_time, end_time, ISSUERS)

    rejected_job_models_RFP_data = req_for_payment.get_dashboard_data(test_cookie, start_time, end_time, ISSUERS)
    
    api_gen_target_data = target_gen.get_dashboard_data(test_cookie, start_time, end_time, ISSUERS)
    
    refunds_data, payment_flows_data = buisness.get_dashboard_data(test_cookie, start_time, end_time, ISSUERS)

    api_termination_data = api_terminate.get_dashboard_data(test_cookie, start_time, end_time, ISSUERS)

    response_data = {
        'invoice': rejected_job_models_invoice_data,
        'RFP' : rejected_job_models_RFP_data,
        'gen_target' : api_gen_target_data,
        'payment_flow' :  payment_flows_data,
        'refunds' : refunds_data,
        'api_terminate': api_termination_data
    }

    print("this is the response data:\n", json.dumps(response_data, indent=4))

    formatted_date = start_time[:10]
    print("formatted date", formatted_date)

    # db_connection = ""
    update_dashboard_table(db_connection, start_time, response_data, ISSUERS)

    db_connection.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps("success!!")
    }

lambda_handler(1,1)
