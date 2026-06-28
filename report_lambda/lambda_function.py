import boto3
import json
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    response = table.scan()

    customers = response["Items"]

    report = {

        "generatedDate": datetime.utcnow().isoformat(),

        "totalCustomers": len(customers),

        "customers": customers

    }

    file_name = datetime.utcnow().strftime("%Y-%m-%d") + ".json"

    s3.put_object(

        Bucket=BUCKET_NAME,

        Key=f"reports/{file_name}",

        Body=json.dumps(report),

        ContentType="application/json"

    )

    return {

        "statusCode": 200,

        "message": "Daily Report Generated",

        "totalCustomers": len(customers)

    }