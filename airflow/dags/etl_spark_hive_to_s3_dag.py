"""
Airflow DAG to submit a Spark job that reads from Hive and writes to MinIO S3.
"""

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

with DAG(
    dag_id='etl_spark_hive_to_s3',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False,
    description='ETL: Spark reads from Hive and writes to MinIO S3'
) as dag:

    run_spark_etl = SparkSubmitOperator(
        task_id='export_hive_to_s3',
        application='/opt/airflow/dags/scripts/export_hive_to_s3_job.py',
        conn_id='spark_default',
        executor_memory='2g',
        total_executor_cores=2,
        name='export_hive_to_s3_job',
        verbose=True
    )