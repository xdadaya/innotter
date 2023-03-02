import boto3
from microservice.settings import settings


class PageStatisticsDatabase:
    dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_DYNAMODB_REGION,
                              aws_access_key_id=settings.AWS_ACCESS_KEY,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    table = dynamodb.Table(settings.AWS_DYNAMODB_TABLE_NAME)

    @classmethod
    def get_item(cls, pk):
        return cls.table.get_item(Key={"page_id": pk})["Item"]

