import datetime
import io

import boto3
from botocore.client import Config

from config import S3_CONF


class S3_client:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=S3_CONF['access_key'],
            aws_secret_access_key=S3_CONF['secret_key'],
            endpoint_url=S3_CONF['endpoint'],
        )

        self.bucket = S3_CONF['bucket']

        response = self.client.list_buckets()

        if self.bucket in [b["Name"] for b in response["Buckets"]]:
            print(f"🪣 Bucket {self.bucket} already exists")
        else:
            print(f"🪣 Creating bucket {self.bucket}")
            self.client.create_bucket(Bucket=self.bucket)
            self.client.put_bucket_cors(
                Bucket=self.bucket,
                CORSConfiguration={
                    "CORSRules": [
                        {
                            "AllowedMethods": ["GET", "HEAD"],
                            "AllowedOrigins": [
                                "*",
                            ],
                            "ExposeHeaders": ["*"],
                            "AllowedHeaders": ["Content-Type", "Authorization"],
                        }
                    ]
                },
            )

    def upload(self, content, filename, mime_type):
        print(f"⬆️ Uploading file {filename}")
        self.client.upload_fileobj(
            content,
            self.bucket,
            filename,
            ExtraArgs={
                "ContentType": mime_type,
                "ACL": "public-read",
            },
        )

    def get(self, filename):
        print(f"⬇️ Downloading {filename}")
        output = io.BytesIO()
        self.client.download_fileobj(self.bucket, filename, output)
        return output.getvalue()

    def exists(self, filename):
        response = self.client.list_objects(Bucket=self.bucket)
        return "Contents" in response and filename in [
            item["Key"]
            for item in self.client.list_objects_v2(
                Bucket=self.bucket, Prefix=filename
            )["Contents"]
        ]
