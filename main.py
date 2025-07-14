from etl.generate_data import generate_multiple_users
from etl.user_profiles import USER_PROFILES
from upload_to_s3 import upload_all
import logging

# --- Set up logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

if __name__ == "__main__":
    logging.info("Starting CGM pipeline...")

    generate_multiple_users(USER_PROFILES)
    logging.info("Data generation completed.")

    upload_all()
    logging.info("Upload to S3 completed.")

    logging.info("Pipeline finished successfully.")
