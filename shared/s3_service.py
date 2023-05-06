from datetime import datetime

import boto3
from rest_framework.serializers import ImageField

import shared.aws_credentials as aws_creds


class S3Service:
    @staticmethod
    def upload_file(img: ImageField) -> str:
        full_name = img.name
        file_name = full_name[:full_name.rindex(".")]
        file_extension = full_name[full_name.rindex("."):]
        file_key = file_name + str(int(datetime.now().timestamp())) + file_extension
        session = boto3.session.Session(aws_access_key_id=aws_creds.AWS_ACCESS_KEY,
                                        aws_secret_access_key=aws_creds.AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        s3.Bucket(aws_creds.AWS_S3_BUCKET_NAME).put_object(Key=file_key, Body=img)
        url = f"{aws_creds.AWS_S3_BUCKET_BASE_FILE_URL}{file_key}"
        return url


    @staticmethod
    def delete_file(file_key: str) -> None:
        session = boto3.session.Session(aws_access_key_id=aws_creds.AWS_ACCESS_KEY,
                                        aws_secret_access_key=aws_creds.AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        s3.Object(aws_creds.AWS_S3_BUCKET_NAME, file_key).delete()
