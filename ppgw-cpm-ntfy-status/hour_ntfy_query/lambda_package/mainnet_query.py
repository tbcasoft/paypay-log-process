from collections import defaultdict
from datetime import datetime
import json
import time
import boto3


def get_query_id(client, start_time, end_time):
    
    log_group_name = '/aws/lambda/ppgw-cpm-ntfy-status'

    response = client.start_query(
    logGroupName=log_group_name,
    startTime=start_time, 
    endTime=end_time,
    queryString='\
            fields @timestamp, @message \
            | filter @message like "HIVEX" \
            | parse @message "* INFO" as id \
            | parse @message "merchantName*," as merchant \
            | parse @message "value*}" as val \
            | parse @message "otcRequestId*," as otc \
            | parse @message "resultCode*," as result \
            | fields replace(merchant, ":", "") as merchantName \
            | fields replace(val, ":", "") as value \
            | fields replace(otc, ":", "") as otcRequestId \
            | fields replace(result, ":", "") as resultCode\
            | display @timestamp, id, merchantName, value, otcRequestId, resultCode',
    )
            
    query_id = response['queryId']

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
    
    # role_arn = 'arn:aws:iam::281553677985:role/fe-log-automation'
    
    # sts_client = boto3.client('sts')
    
    # assumed_role = sts_client.assume_role(
    #     RoleArn=role_arn,
    #     RoleSessionName='CrossAccountLambdaSession'
    # )
    
    # credentials = assumed_role['Credentials']
    
    c = boto3.client(
        'logs',
        # aws_access_key_id=credentials['AccessKeyId'],
        # aws_secret_access_key=credentials['SecretAccessKey'],
        # aws_session_token=credentials['SessionToken'],
        region_name='ap-northeast-1'
    )
    
    id = get_query_id(client=c, start_time=s_time, end_time=e_time)
    log_data = wait_and_get_query(client=c, query_id=id)
    
    event_streams = defaultdict(dict)
    for event in log_data[::-1]:
        id = event[1]["value"]
        otcId = event[4]["value"].replace("\"", "")
        if id == otcId:
            event_streams[id] = {
                event[0]["field"].replace("@", "") : event[0]["value"],
                event[2]["field"]: event[2]["value"].replace("\"", ""), 
                event[3]["field"]: event[3]["value"].replace("\"", ""), 
                event[4]["field"]: otcId, 
                event[5]["field"]: event[5]["value"].replace("\"", "")
            }
    
    # print(json.dumps(event_streams, indent=4))
    return event_streams


    
