import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info(f"Received Event: {json.dumps(event)}")

    aadhaar = event.get("aadhaar")

    if not aadhaar:
        raise Exception("Aadhaar Number Missing")

    # Dummy KYC Validation
    if len(aadhaar) == 12 and aadhaar.isdigit():

        event["kycStatus"] = "VERIFIED"

        logger.info("KYC Verified Successfully")

        return event

    else:

        raise Exception("KYC Verification Failed")