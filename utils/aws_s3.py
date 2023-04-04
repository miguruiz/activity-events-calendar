import boto3
import re

def read_from_s3(s3_path):

    s3 = boto3.client('s3')

    file_name = re.search(r'[^/]+$', s3_path).group(0)

    bucket_name =  s3_path[:-len(file_name)].replace("s3://","").replace("/","")

    # read file from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = response['Body'].read().decode('utf-8')
    return file_content


def write_to_s3(s3_path, content):
    s3 = boto3.client('s3')

    file_name = re.search(r'[^/]+$', s3_path).group(0)
    bucket_name = s3_path[:-len(file_name)].replace("s3://", "").replace("/", "")

    s3.put_object(Bucket=bucket_name, Key=file_name, Body=content)