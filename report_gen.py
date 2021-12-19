import boto3
import pandas as pd

s3_resource = boto3.resource(
    service_name='s3',
    region_name='',
    aws_access_key_id='',
    aws_secret_access_key=''
)

s3_session = boto3.client(
    service_name='s3',
    region_name='',
    aws_access_key_id='',
    aws_secret_access_key=''
)

dest_bucket = s3_resource.Bucket('fss-test-logs')

def log_collector():
    files_to_scan = []
    #files_to_scan.append(['Name', 'File URL', 'Scan Successful?', 'Bytes', 'Findings', 'Scanner status', 'Time of Scan'])

    for each_file in dest_bucket.objects.all():
        #print(each_file.key)
        body_text = each_file.get()['Body'].read()
        body_text = body_text.decode('utf-8')
        print(body_text)
        body_text = body_text.replace(", 'type':",": type:")
        print(body_text)

        files_to_scan.append(body_text)

    df = pd.DataFrame(files_to_scan, columns=['Name'])
    df[['Name', 'File URL', 'Scan Successful?', 'Bytes', 'Findings', 'Scanner status', 'Time of Scan']] = df['Name'].str.split(',', expand=True)

    print(df.head())
    df.to_csv('test_extract.csv')

log_collector()
