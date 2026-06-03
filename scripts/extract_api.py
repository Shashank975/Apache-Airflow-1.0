# scripts/extract_api.py

import requests


DATAUSA_API_URL = (
    "https://api.datausa.io/tesseract/data.jsonrecords"
    "?cube=acs_yg_total_population_5"
    "&drilldowns=State,Year"
    "&measures=Population"
    "&include=Year:2023"
    "&limit=100000"
)


def extract_data():

    response = requests.get(
        DATAUSA_API_URL,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["data"]