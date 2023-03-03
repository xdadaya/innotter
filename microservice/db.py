import boto3

from microservice.models import PageStatistics
from microservice.settings import settings


class PageStatisticsDatabase:
    dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_DYNAMODB_REGION,
                              aws_access_key_id=settings.AWS_ACCESS_KEY,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    table = dynamodb.Table(settings.AWS_DYNAMODB_TABLE_NAME)

    @classmethod
    def get_item(cls, pk: str) -> PageStatistics:
        return cls.table.get_item(Key={"page_id": pk})["Item"]

    @classmethod
    def create_item(
        cls, page_id: str, owner_id: str, likes_amount: int, followers_amount:int, posts_amount: int
    ) -> None:
        cls.table.put_item(
            Item={
                'page_id': page_id,
                'owner_id': owner_id,
                'likes_amount': likes_amount,
                'followers_amount': followers_amount,
                'posts_amount': posts_amount,
            },
        )

    @classmethod
    def update_item(cls, page_id: str, likes_amount: int, followers_amount: int, posts_amount: int) -> None:
        cls.table.update_item(
            Key={'page_id': page_id},
            UpdateExpression="set likes_amount = :la, followers_amount: :fa, posts_amount: :pa",
            ExpressionAttributeValues={
                ':la': likes_amount,
                ':fa': followers_amount,
                ':pa': posts_amount,
            },
        )

    @classmethod
    def delete_item(cls, page_id: str) -> None:
        cls.table.delete_item(Key={'page_id': page_id})
