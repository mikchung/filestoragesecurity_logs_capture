import boto3
import pandas as pd

s3_resource = boto3.resource(
    service_name='s3',
    region_name='ap-southeast-2',
    aws_access_key_id='AKIAUFMJAYJVYCEV6RBD',
    aws_secret_access_key='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'
)

s3_session = boto3.client(
    service_name='s3',
    region_name='ap-southeast-2',
    aws_access_key_id='AKIAUFMJAYJVYCEV6RBD',
    aws_secret_access_key='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'
)

dest_bucket = s3_resource.Bucket('fss-test-logs')

def log_collector():
    files_to_scan = []
    #files_to_scan.append(['Name', 'File URL', 'Scan Successful?', 'Bytes', 'Findings', 'Scanner status', 'Time of Scan'])

    for each_file in dest_bucket.objects.all():
        #print(each_file.key)
        body_text = each_file.get()['Body'].read()
        body_text = body_text.decode('utf-8')
        files_to_scan.append(body_text)

    df = pd.DataFrame(files_to_scan, columns=['Name'])
    #df = df[0].str.decode('utf-8')
    df['Name'].str.split(',', expand=True)

    #print(files_to_scan)

    print(df.head())
    df.to_csv('test_extract.csv')

log_collector()
