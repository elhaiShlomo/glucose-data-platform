from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from cgm_utils.athena_utils import repair_athena_table
from etl.generate_data import generate_multiple_users
from etl.user_profiles import USER_PROFILES
from upload_to_s3 import upload_all


default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    dag_id="cgm_data_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    description="CGM data pipeline DAG",
    tags=["cgm", "s3", "athena"]
) as dag:

    generate_data = PythonOperator(
        task_id="generate_cgm_data",
        python_callable=generate_multiple_users,
        op_kwargs={"user_profiles": USER_PROFILES}
    )

    upload_to_s3 = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_all
    )

    repair_athena = PythonOperator(
        task_id="repair_athena_partitions",
        python_callable=repair_athena_table
    )

    generate_data >> upload_to_s3 >> repair_athena
