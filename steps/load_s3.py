import boto3, json, os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def upload_raw(data):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    key = f"raw/weather_{ts}.json"
    s3.put_object(
        Bucket=os.getenv("AWS_BUCKET"),
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json"
    )
    print(f"  S3 upload done: {key}")