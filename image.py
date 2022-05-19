import logging
import boto3
from botocore.exceptions import ClientError
import os


# Upload file to AWS S3 Bucket
def s3_upload_file(s3_client, file_name, bucket, object_name):
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)


# Download file from AWS S3 Bucket
def s3_download_file(file_name, bucket):
    s3 = boto3.resource('s3',
                        aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                        aws_secret_access_key=os.environ['S3_SECRET_KEY'])
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def generate_url(s3_client, file_name: str, bucket: str, timeout: int):
    return s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': file_name},
                                            ExpiresIn=timeout)
