import logging
import threading

import functions_framework
import google.cloud.logging
from faker import Faker
from google.cloud import bigquery

# Instantiates Cloud Logging client
logging_client = google.cloud.logging.Client()
# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default, this captures all logs
# at INFO level and higher
logging_client.setup_logging()

# Initialize Faker
fake = Faker()

# Initialize BigQuery client
client = bigquery.Client()


def generate_mock_data(num_records):
    mock_data = []
    for _ in range(num_records):
        data = {
            'name': fake.name(),
            'age': fake.random_int(min=18, max=99),
            'country': fake.country()
        }
        mock_data.append(data)
    return mock_data


def insert_mock_data(data):
    errors = client.insert_rows_json('report.people', data)
    if errors:
        logging.error(f'Encountered errors while inserting rows: {errors}')
    else:
        logging.info(f'Successfully inserted {len(data)} records into {data}')


def job(num_records):
    data = generate_mock_data(num_records)
    insert_mock_data(data)


@functions_framework.http
def fake_data(request):
    num_records = request.json.get('num_records', 100_000)  # Default to 100k if not provided
    threading.Thread(target=job(num_records)).start()
    return '', 202