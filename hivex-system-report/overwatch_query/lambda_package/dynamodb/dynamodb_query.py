import boto3

def query_db():
    
    db_client = boto3.client('dynamodb', region_name='ap-northeast-1')
    
    table_name = 'PPGW-STORE-TABLE'
    
    meta_data = db_client.describe_table(TableName=table_name)
    
    item_count = meta_data["Table"]["ItemCount"]

    return item_count