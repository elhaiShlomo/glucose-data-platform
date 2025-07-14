from datetime import datetime, timedelta
import random
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)


def generate_cgm_data(user_id, mean, sigma, days=2):
    now = datetime.now().replace(second=0, microsecond=0)
    created_at = datetime.now().isoformat()
    records = []

    for i in range(days * 24 * 12):  # Every 5 minutes for N days
        timestamp = now - timedelta(minutes=5 * i)
        glucose = round(random.gauss(mean, sigma), 1)
        glucose = max(40.0, min(glucose, 300.0))
        records.append({
            "user_id": user_id,
            "timestamp": timestamp.isoformat(),
            "glucose_mgdl": glucose,
            "created_at": created_at
        })

    return pd.DataFrame(records)


def generate_multiple_users(user_profiles, days=2):
    os.makedirs("data", exist_ok=True)
    for user_id, profile in user_profiles.items():
        df = generate_cgm_data(user_id, profile["mean"], profile["sigma"], days)
        path = f"data/{user_id}_cgm.csv"
        df.to_csv(path, index=False)
        logger.info(f"{user_id} ({profile['profile']}) → {len(df)} rows → {path}")
