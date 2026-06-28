import json
import logging
import boto3
import os
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    try:

        logger.info(json.dumps(event))

        customer = {

            "mobileNumber": event["mobileNumber"],
            "requestId": event["requestId"],
            "name": event["name"],
            "email": event["email"],
            "city": event["city"],
            "aadhaar": event["aadhaar"],
            "plan": event["plan"],
            "kycStatus": event["kycStatus"],
            "status": "ACTIVE",
            "createdDate": datetime.utcnow().isoformat()
        }

        table.put_item(Item=customer)

        logger.info("Customer inserted into DynamoDB")

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"customers/{customer['mobileNumber']}.json",
            Body=json.dumps(customer),
            ContentType="application/json"
        )

        logger.info("Customer Backup uploaded to S3")

        return {

            "statusCode": 200,

            "customer": customer

        }

    except Exception as e:

        logger.exception(str(e))

        raise