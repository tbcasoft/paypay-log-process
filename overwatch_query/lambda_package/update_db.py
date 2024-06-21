from datetime import datetime, timezone
import json


def update_dashboard_table(connection, start_time, response_data, issuers):

    cursor = connection.cursor()

    update_table = '''
    INSERT INTO daily_overwatch_dashboard 
    (time, 
    issuer, 
    rejected_job_models_invoice_count, 
    rejected_jobmodels_RFP_count, 
    api_gen_target_count, 
    payments_CPM_count, 
    payments_CPM_dest_amount, 
    payments_MPM_count, 
    payments_MPM_dest_amount, 
    refunds_count, 
    refunds_sum_of_amount,
    termination_OPT_OUT,
    termination_EXPIRED_CODE,
    termination_ACQUIRER_VALIDATION)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    formatted_date = start_time[:10]
    print("formatted date", formatted_date)

    # issuers = list(response_data["invoice"].keys())[::-1]
    data = []

    print(json.dumps(response_data, indent=4))

    for issuer in issuers:

        rejected_job_models_invoice_count = response_data["invoice"][issuer]["rejected_count"]
        rejected_jobmodels_RFP_count = response_data["RFP"][issuer]["rejected_count"]
        api_gen_target_count = response_data["gen_target"][issuer]["count"]
        
        payment_flow = response_data["payment_flow"]

        payments_CPM_count = payment_flow["CPM"][issuer]["count"]
        payments_CPM_dest_amount = payment_flow["CPM"][issuer]["dest_amount"]
        payments_MPM_count = payment_flow["MPM"][issuer]["count"]
        payments_MPM_dest_amount = payment_flow["MPM"][issuer]["dest_amount"]
        refunds_count = response_data["refunds"][issuer]["count"]
        refunds_sum_of_amount = response_data["refunds"][issuer]["sum_of_amount"]

        api_terminate = response_data["api_terminate"]

        termination_OPT_OUT = api_terminate["OPT_OUT"][issuer]
        termination_EXPIRED_CODE = api_terminate["EXPIRED_CODE"][issuer]
        termination_ACQUIRER_VALIDATION = api_terminate["ACQUIRER_VALIDATION"][issuer]

        data.append((formatted_date, issuer, rejected_job_models_invoice_count, rejected_jobmodels_RFP_count,
                     api_gen_target_count, payments_CPM_count, payments_CPM_dest_amount, payments_MPM_count,
                     payments_MPM_dest_amount, refunds_count, refunds_sum_of_amount,
                     termination_OPT_OUT, termination_EXPIRED_CODE, termination_ACQUIRER_VALIDATION))

    cursor.executemany(update_table, data)

    connection.commit()
    cursor.close()