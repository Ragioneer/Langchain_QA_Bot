import boto3, botocore
import os
from variables import access_key,secret_access_key,bucket_name,object_name,file_name

s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key
)


# Here bucket_name is the name of the bucket, object_name is the name of the of the object,
# while file_name is the name of the file to be created in your local directory after download
s3.download_file(bucket_name, object_name, file_name) 


