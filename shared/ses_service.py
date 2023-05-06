import boto3
from celery import shared_task

import shared.aws_credentials as aws_creds


class SESService:
    @staticmethod
    @shared_task
    def send_emails(emails: list[str], base_domain: str, post_content: str, page_id: str) -> None:
        message_data = "New post wow wow wow"
        message_text = f"New post [{post_content}] on page {base_domain}/api/pages/{page_id}"
        session = boto3.session.Session(aws_access_key_id=aws_creds.AWS_ACCESS_KEY,
                                        aws_secret_access_key=aws_creds.AWS_SECRET_ACCESS_KEY)
        client = session.client('ses', region_name=aws_creds.AWS_SES_REGION)
        client.send_email(
            Destination={'ToAddresses': emails},
            Message={
                'Subject': {
                    'Data': message_data,
                    'Charset': "UTF-8"
                },
                'Body': {
                    'Text': {
                        'Data': message_text,
                        'Charset': "UTF-8"
                    },
                }
            },
            Source=aws_creds.AWS_SES_SOURCE,
        )