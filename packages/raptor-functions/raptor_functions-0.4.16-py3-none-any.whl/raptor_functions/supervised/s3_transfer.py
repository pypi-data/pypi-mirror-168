import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from decouple import config


#  AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
#  AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

AWS_ACCESS_KEY = config('AWS_ACCESS_KEY')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')


def upload_file(file_name, bucket):
    """_summary_

    Args:
        file_name (_type_): _description_
        bucket (_type_): _description_

    Returns:
        _type_: _description_
    """
    object_name = file_name
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response




def download_file(file_name, bucket):
    """_summary_

    Args:
        file_name (_type_): _description_
        bucket (_type_): _description_

    Returns:
        _type_: _description_
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output




def list_files(bucket):
    """_summary_

    Args:
        bucket (_type_): _description_

    Returns:
        _type_: _description_
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents