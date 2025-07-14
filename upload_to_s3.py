
import boto3
from pathlib import Path
import logging
import pandas as pd
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# --- Config ---
BUCKET_NAME = "cgm-data-pipeline"
DATA_FOLDER = Path("data")
AWS_PROFILE = "personal"

# --- AWS session and client ---
session = boto3.Session(profile_name=AWS_PROFILE)
s3 = session.client("s3")


def upload_file(df: pd.DataFrame, user_id: str):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    for date, group in df.groupby("date"):
        date_obj = pd.to_datetime(date)
        date_str = date_obj.strftime("%Y-%m-%d")
        file_date_str = date_obj.strftime("%Y%m%d")
        filename = f"{file_date_str}_{user_id}_cgm.parquet"
        temp_path = DATA_FOLDER / filename

        # Drop partition columns before writing Parquet
        group = group.drop(columns=["user_id", "date"])
        group.to_parquet(temp_path, index=False)

        s3_key = f"user_id={user_id}/date={date_str}/{filename}"

        try:
            s3.upload_file(str(temp_path), BUCKET_NAME, s3_key)
            logger.info(f"Uploaded {filename} → s3://{BUCKET_NAME}/{s3_key}")
        except ClientError:
            logger.error(f"Failed to upload {filename}", exc_info=True)
        finally:
            temp_path.unlink(missing_ok=True)


def upload_all():
    if not DATA_FOLDER.exists():
        logger.error("'data/' folder not found.")
        return

    for file in DATA_FOLDER.glob("*.csv"):
        try:
            user_id = "_".join(file.stem.split("_")[:2])
            df = pd.read_csv(file)
            upload_file(df, user_id)
        except Exception as e:
            logger.error(f"Error processing {file.name}: {e}")
