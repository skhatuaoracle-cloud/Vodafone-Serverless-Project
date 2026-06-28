import json
import uuid
import logging
from datetime import datetime

import boto3

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS Clients
s3 = boto3.client("s3")
sqs = boto3.client("sqs")

# Environment Variables
BUCKET_NAME = "vodafone-customer-data"
QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/123456789012/VodafoneCustomerQueue"


def lambda_handler(event, context):

    try:
        logger.info("Received Event: %s", json.dumps(event))

        body = json.loads(event["body"])

        required_fields = [
            "name",
            "email",
            "city",
            "aadhaar",
            "plan"
        ]

        # Validate request
        for field in required_fields:
            if field not in body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": f"{field} is required"
                    })
                }

        request_id = str(uuid.uuid4())

        customer_data = {
            "requestId": request_id,
            "name": body["name"],
            "email": body["email"],
            "city": body["city"],
            "aadhaar": body["aadhaar"],
            "plan": body["plan"],
            "status": "PENDING",
            "createdDate": datetime.utcnow().isoformat()
        }

        # Upload JSON to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"requests/{request_id}.json",
            Body=json.dumps(customer_data),
            ContentType="application/json"
        )

        logger.info("Uploaded request to S3")

        # Send Message to SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(customer_data)
        )

        logger.info("Message Sent to SQS")

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Customer Registration Successful",
                "requestId": request_id
            })
        }

    except Exception as e:

        logger.exception("Unexpected Error")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }