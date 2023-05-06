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
    def create_item(cls, page_statistics: PageStatistics) -> None:
        cls.table.put_item(
            Item={
                'page_id': page_statistics.page_id,
                'owner_id': page_statistics.owner_id,
                'likes_amount': page_statistics.likes_amount,
                'followers_amount': page_statistics.followers_amount,
                'posts_amount': page_statistics.posts_amount,
            },
        )

    @classmethod
    def update_item(cls, page_statistics: PageStatistics) -> None:
        item = PageStatisticsDatabase.get_item(page_statistics.page_id)
        likes_amount = page_statistics.likes_amount
        posts_amount = page_statistics.posts_amount
        followers_amount = page_statistics.followers_amount
        if likes_amount is None:
            likes_amount = item["likes_amount"]
        if followers_amount is None:
            followers_amount = item["followers_amount"]
        if posts_amount is None:
            posts_amount = item["posts_amount"]
        cls.table.update_item(
            Key={'page_id': page_statistics.page_id},
            UpdateExpression="set likes_amount = :la, followers_amount = :fa, posts_amount = :pa",
            ExpressionAttributeValues={
                ':la': likes_amount,
                ':fa': followers_amount,
                ':pa': posts_amount,
            },
        )

    @classmethod
    def delete_item(cls, page_statistics: PageStatistics) -> None:
        cls.table.delete_item(Key={'page_id': page_statistics.page_id})
