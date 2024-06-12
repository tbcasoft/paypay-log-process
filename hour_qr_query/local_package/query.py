from collections import defaultdict
import json
import time
import boto3


def get_query_id(client, start_time, end_time):
    
    log_group_name = '/aws/lambda/ppgw-resolve-qr'

    response = client.start_query(
    logGroupName=log_group_name,
    startTime=start_time, 
    endTime=end_time,
    queryString='\
            fields @timestamp, @message \
            | filter @message like "target" or @message like "resultCode" \
            | parse @message "* INFO" as id \
            | parse @message "target*qr*}" as _, qrcode \
            | parse @message "resultCode*," as resultCode \
            | fields replace(qrcode, ":", "") as qr \
            | fields replace(resultCode, ":", "") as result\
            | display @timestamp, id, qr, result', 
    )
            
    query_id = response['queryId']

    print("Query ID:", query_id)
    return query_id


def wait_and_get_query(client, query_id):
    while True:
        time.sleep(1)
        results = client.get_query_results(queryId=query_id)
        if results["status"] in [
            "Complete",
            "Failed",
            "Cancelled",
            "Timeout",
            "Unknown",
        ]:
            return results.get("results", [])

def get_query(s_time, e_time):
    c = boto3.client('logs', region_name='ap-northeast-1')
    id = get_query_id(client=c, start_time=s_time, end_time=e_time)
    log_data = wait_and_get_query(client=c, query_id=id)
    
    event_streams = defaultdict(dict)
    for event in log_data[::-1]:
        id = event[1]["value"]
        if id not in event_streams:
            event_streams[id] = {
                event[0]["field"].replace("@", "") : event[0]["value"],
                event[2]["field"]: event[2]["value"].replace("\"", "") 
            }
        else:
            event_streams[id]["result"] = event[-2]["value"].replace("\"", "")
    
    print(json.dumps(event_streams, indent=4))
    return event_streams
