import boto3
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)

AWS_PROFILE = os.getenv("AWS_PROFILE")
AWS_REGION = os.getenv("AWS_REGION")
ATHENA_DATABASE = os.getenv("ATHENA_DATABASE")
ATHENA_TABLE = os.getenv("ATHENA_TABLE")
ATHENA_OUTPUT = os.getenv("ATHENA_OUTPUT")


def repair_athena_table():
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    athena = session.client("athena")

    query = f"MSCK REPAIR TABLE {ATHENA_TABLE}"
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": ATHENA_DATABASE},
        ResultConfiguration={"OutputLocation": ATHENA_OUTPUT}
    )

    query_id = response["QueryExecutionId"]
    logger.info(f"Started MSCK REPAIR TABLE with Query ID: {query_id}")
