import boto3
import re

def read_from_s3(s3_path):
    """
    Reads the content of a file from an S3 bucket.

    Args:
        s3_path (str): The S3 path of the file in the format "s3://<bucket_name>/<file_name>".

    Returns:
        str: The content of the file as a string.

    Raises:
        Exception: If there is an error while reading the file from S3.
    """
    s3 = boto3.client('s3')

    file_name = re.search(r'[^/]+$', s3_path).group(0)

    bucket_name =  s3_path[:-len(file_name)].replace("s3://","").replace("/","")

    # read file from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = response['Body'].read().decode('utf-8')
    return file_content


def write_to_s3(s3_path, content):
    """
     Writes the content to a file in an S3 bucket.

     Args:
         s3_path (str): The S3 path of the file in the format "s3://<bucket_name>/<file_name>".
         content (str): The content to be written to the file.

     Raises:
         Exception: If there is an error while writing the content to S3.
     """
    s3 = boto3.client('s3')

    file_name = re.search(r'[^/]+$', s3_path).group(0)
    bucket_name = s3_path[:-len(file_name)].replace("s3://", "").replace("/", "")

    s3.put_object(Bucket=bucket_name, Key=file_name, Body=content)