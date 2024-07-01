
def update_issuers_table(connection, start_time, response_data, issuers, acquiers):

    cursor = connection.cursor()

    update_table = '''
    INSERT INTO hivex_system_report_issuers 
    (week_date,
    acquier,
    issuer, 
    get_invoice_latency_median, 
    get_invoice_latency_p99, 
    pay_latency_median, 
    pay_latency_p99, 
    conf_page_latency_median, 
    conf_page_latency_p99)
    VALUES
        (%s, %s, %s, ROUND(%s, 1), ROUND(%s, 1), ROUND(%s, 1), ROUND(%s, 1), ROUND(%s, 1), ROUND(%s, 1))
    '''


    formatted_date = start_time[:10]

    data = []
    acquier = acquiers[0]

    for issuer in issuers:
        api_elapsed = response_data['get_invoice_latency_data'][issuer]
        pay_latency = response_data['pay_latency_data'][issuer]
        conf_page_latency = response_data['conf_page_latency_data'][issuer]
        
        get_invoice_latency_median = api_elapsed['median']
        get_invoice_latency_p99 = api_elapsed['p99']
        pay_latency_median = pay_latency['median']
        pay_latency_p99 = pay_latency['p99']
        conf_page_latency_median = conf_page_latency['median']
        conf_page_latency_p99 = conf_page_latency['p99']
        
        data.append((formatted_date, acquier, issuer, 
                    get_invoice_latency_median, get_invoice_latency_p99, 
                    pay_latency_median, pay_latency_p99, 
                    conf_page_latency_median, conf_page_latency_p99))
    
    cursor.executemany(update_table, data)

    connection.commit()
    cursor.close()
    
    
def update_weekly_stats_table(connection, start_time, response_data):

    cursor = connection.cursor()

    update_table = '''
    INSERT INTO hivex_system_report_weekly_stat 
    (week_date,
    data_name,
    data_value)
    VALUES
        (%s, %s, %s)
    '''

    formatted_date = start_time[:10]

    data = []
    
    weekly_stats = response_data['weekly_stats']
    
    for key in weekly_stats:
        data_name = key
        data_value = weekly_stats[key]
        
        data.append((formatted_date, data_name, data_value))
    
    cursor.executemany(update_table, data)

    connection.commit()
    cursor.close()