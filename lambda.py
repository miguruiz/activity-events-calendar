import os
import sys
import json

# Activate the venv
venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')

# Add the zip file to sys.path
zip_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'my_lambda.zip'))
sys.path.append(zip_file)

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

def download_s3_files():
    import boto3

    s3 = boto3.client('s3')

    bucket_name = 'activity-events-calendar'
    key = ['personal-mrn-d9d05a8cd966.json','config.ini']
    local_filename = '/tmp/'
    for k in key:
        s3.download_file(bucket_name, k, local_filename + k)
def lambda_handler(event, context):
    import activity_scrapper
    download_s3_files()
    activity_scrapper.main()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
