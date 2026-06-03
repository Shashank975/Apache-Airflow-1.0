# scripts/save_csv.py

from datetime import datetime
import pandas as pd


def save_to_csv(records):
    """
    Save records to CSV with a timestamped filename.
    """

    df = pd.DataFrame(records)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"/opt/airflow/data/datausa_population_{timestamp}.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(f"CSV file created successfully: {output_file}")