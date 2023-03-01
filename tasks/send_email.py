from innotter import settings
import dramatiq
import boto3


@dramatiq.actor
def send_emails(emails: list[str], base_domain: str) -> None:
    message_data = "New post wow wow wow"
    message_text = f"New post on page {base_domain}/"
    print(message_text)
    with open("test.txt", "w") as file:
        file.write("asd")
    client = boto3.client('ses', settings.AWS_SES_REGION)
    client.send_email(
        Source=settings.AWS_SES_SOURCE,
        Destination={'ToAddresses': emails},
        Message={
            'Subject': {'Data': message_data},
            'Body': {
                'Text': {'Data': message_text},
            }
        }
    )