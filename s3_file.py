import logging
import boto3
from botocore.exceptions import ClientError
import os

# Upload file to AWS S3 Bucket
def s3_upload_file(file_name, bucket, object_name):
    s3_client = boto3.client('s3',
                      aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                      aws_secret_access_key=os.environ['S3_SECRET_KEY'])

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)

    return response

# Download file from AWS S3 Bucket
def s3_download_file(file_name, bucket):

    s3 = boto3.resource('s3',
                      aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                      aws_secret_access_key=os.environ['S3_SECRET_KEY'])
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output