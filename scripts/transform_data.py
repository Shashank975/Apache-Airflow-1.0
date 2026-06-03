# scripts/transform_data.py

from datetime import date


def convert_to_lowercase(records):
    """
    Convert all string values to lowercase, lowercase column names (keys),
    and add inserted_on and source_name columns.
    """

    transformed_records = []
    current_date = date.today().isoformat()

    for record in records:

        transformed_record = {}

        for key, value in record.items():
            lower_key = key.lower()
            if isinstance(value, str):
                transformed_record[lower_key] = value.lower()
            else:
                transformed_record[lower_key] = value

        # Add the two additional columns
        transformed_record["inserted_on"] = current_date
        transformed_record["source_name"] = "test"

        transformed_records.append(transformed_record)

    return transformed_records