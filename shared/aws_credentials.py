import os

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.environ.get("AWS_S3_REGION")
AWS_SES_REGION = os.environ.get("AWS_SES_REGION")
AWS_SES_SOURCE = os.environ.get("AWS_SES_SOURCE")

AWS_S3_BUCKET_BASE_FILE_URL = f"https://s3-{AWS_S3_REGION}.amazonaws.com/{AWS_S3_BUCKET_NAME}/"
