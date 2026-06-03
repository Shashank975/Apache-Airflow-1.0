from airflow.sdk import dag, task
from datetime import datetime

from scripts.extract_api import extract_data
from scripts.transform_data import convert_to_lowercase
from scripts.save_csv import save_to_csv
from scripts.save_db import save_to_db


@dag(
    dag_id="api_processer",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
)
def first_dag():

    @task
    def extract_task():
        return extract_data()

    @task
    def transform_task(data):
        return convert_to_lowercase(data)

    @task
    def load_task(data):
        save_to_csv(data)

    @task
    def load_db_task(data):
        save_to_db(data)

    raw_data = extract_task()

    transformed_data = transform_task(raw_data)

    load_task(transformed_data)
    load_db_task(transformed_data)


first_dag()