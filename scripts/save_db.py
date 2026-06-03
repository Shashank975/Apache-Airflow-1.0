# scripts/save_db.py

import pandas as pd
# pyrefly: ignore [missing-import]
from airflow.providers.postgres.hooks.postgres import PostgresHook


def save_to_db(records, table_name="datausa_population", conn_id="postgres_local"):
    """
    Save records to PostgreSQL database.
    If the table does not exist, it will be created.
    If it exists, data will be appended.
    """
    if not records:
        print("No records to save to the database.")
        return

    # Convert records (list of dicts) to a DataFrame
    df = pd.DataFrame(records)

    # Instantiate the Postgres Hook from Airflow
    hook = PostgresHook(postgres_conn_id=conn_id)
    
    # Retrieve the SQLAlchemy engine to write the data
    engine = hook.get_sqlalchemy_engine()

    # Append to database (creates table if not exists)
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Successfully wrote {len(df)} rows to database table '{table_name}' (append mode).")