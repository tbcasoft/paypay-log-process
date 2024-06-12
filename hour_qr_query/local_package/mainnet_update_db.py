from datetime import datetime, timezone
from analysis import result_analysis

def update_raw_table(connection, log_event_streams):
    cursor = connection.cursor()

    for id, event in log_event_streams.items():
        
        update_table = '''
        INSERT INTO mainnet_hour_qr_raw
        (time, id, qr, result_code)
        VALUES
            (%s, %s, %s, %s)
        '''
        cursor.execute(update_table, (event["timestamp"], id, event["qr"], event["result"]))
    
    connection.commit()
    cursor.close()

def update_analysis_table(connection, start_time, log_event_streams):
    non_unique, unique = result_analysis(event_streams=log_event_streams)

    cursor = connection.cursor()

    update_table = '''
    INSERT INTO mainnet_hour_qr_result 
    (time, SUCCESS, MERCHANT_SUSPENDED, HIVEX_UNAVAILABLE_MERCHANT, Dynamic_QR, P2P, Others, Total,
        SUCCESS_unique, MERCHANT_SUSPENDED_unique, HIVEX_UNAVAILABLE_MERCHANT_unique, 
        Dynamic_QR_unique, P2P_unique, Others_unique, Total_unique)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s)
    '''

    start_time = datetime.fromtimestamp(start_time, timezone.utc)
    formatted_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
    print(formatted_time)
    cursor.execute(update_table, (formatted_time, 
                non_unique["SUCCESS"], non_unique["MERCHANT_SUSPENDED"], non_unique["HIVEX_UNAVAILABLE_MERCHANT"], 
                non_unique["Dynamic_QR"], non_unique["P2P"], non_unique["Others"], non_unique["Total"], 
                unique["SUCCESS"], unique["MERCHANT_SUSPENDED"], unique["HIVEX_UNAVAILABLE_MERCHANT"], 
                unique["Dynamic_QR"], unique["P2P"], unique["Others"], unique["Total"]))

    connection.commit()
    cursor.close()

