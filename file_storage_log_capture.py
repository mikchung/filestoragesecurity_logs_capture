import json
import boto3
from datetime import datetime

bucket_name = 'fss-test-logs'
s3 = boto3.resource('s3')

dynamo_db = boto3.resource('dynamodb', region_name='ap-southeast-2'
dynamo_table = dynamo_db.Table('fss_tracking_logs')

def lambda_handler(event, context):
    
    message_dict = json.loads(event['Records'][0]['Sns']['Message'])
    file_url = message_dict['file_url']
    scanner_status = message_dict['scanner_status_message']
    file_size = message_dict['scanning_result']['TotalBytesOfFile']
    findings = message_dict['scanning_result']['Findings']
    errors = message_dict['scanning_result']['Error']
    time_stamp = str(datetime.now())
    
    #create list to load and load into S3 bucket
    info_list = [file_url, scanner_status, file_size, findings, errors, time_stamp]
    s3.Bucket(bucket_name).put_object(Key=time_stamp, Body=str(info_list))


    #upload into dynamo_db table
    dynamo_table.put_item(
        Item={
            
            'time_snap': time_stamp,
            'errors':errors, 
            'file_size':file_size, 
            'file_url':file_url, 
            'findings':findings, 
            'scanner_status':scanner_status, 
            'time_stamp':time_stamp
            
        }
    )

    
    return {
        'statusCode': 200,
    }
