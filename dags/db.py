from datetime import datetime
from airflow.sdk import dag, task
# pyrefly: ignore [missing-import]
from airflow.providers.postgres.hooks.postgres import PostgresHook


@dag(
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
)
def postgres_connection_test():

    @task
    def test_connection():

        hook = PostgresHook(
            postgres_conn_id="postgres_local"
        )

        result = hook.get_first(
            "SELECT current_database();"
        )

        print(result)

    test_connection()

postgres_connection_test()