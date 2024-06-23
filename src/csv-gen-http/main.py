import logging
from datetime import datetime
from flask import jsonify

import functions_framework
import google.cloud.logging
from google.cloud import bigquery
from google.cloud import storage

# Instantiates BigQuery client
bigquery_client = bigquery.Client()

# Instantiates Cloud Storage client
storage_client = storage.Client()

# Instantiates Cloud Logging client
logging_client = google.cloud.logging.Client()
# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default, this captures all logs
# at INFO level and higher
logging_client.setup_logging()


def get_json_field(request_json, field_name, optional=False):
    if request_json and field_name in request_json:
        return request_json[field_name]
    else:
        if not optional:
            error_message = 'JSON is invalid, or missing "' + field_name + '" property'
            logging.warning(str(error_message))
            raise ValueError(error_message)


def get_data_frame(dataset_name, table_name, fields, filters):
    try:
        query = 'select %s from %s.%s' % (', '.join(fields), dataset_name, table_name)
        if filters:
            query += ' where ' + ' and '.join(filters)
        logging.info('Executing query [{}]'.format(query))
        return bigquery_client.query(query).to_dataframe()
    except Exception as e:
        error_message = 'An exception occurred while querying BigQuery'
        logging.error(error_message + ',\n' + str(e))
        raise IOError(error_message)


def write_csv_file(filename, data_fame):
    try:
        logging.info('Writing csv file [{}]'.format(filename))
        data_fame.to_csv(filename, index=False)
    except Exception as e:
        error_message = 'An exception occurred while writing csv file'
        logging.error(error_message + ',\n' + str(e))
        raise IOError(error_message)


def upload_file_to_bucket(filename, bucket_name):
    try:
        logging.info('uploading [{}] to bucket [{}]'.format(filename, bucket_name))
        blob = storage_client.get_bucket(bucket_name).blob(filename)
        blob.upload_from_filename(filename)
        return filename + ' upload completed'
    except Exception as e:
        error_message = 'An error occurred while uploading file [{}] to bucket [{}]'.format(filename, bucket_name)
        logging.error(error_message + ',\n' + str(e))
        raise IOError(error_message)


@functions_framework.http
def generate_report(request):
    request_json = request.get_json(silent=True)
    # set variables from request Json
    try:
        bucket_name = get_json_field(request_json, 'bucket')
        dataset_name = get_json_field(request_json, 'dataset')
        table_name = get_json_field(request_json, 'table')
        fields = get_json_field(request_json, 'fields')
        filters = get_json_field(request_json, 'filters', optional=True)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    # create and upload csv file to bucket
    try:
        data_fame = get_data_frame(dataset_name, table_name, fields, filters)
        filename = '%s_%s_%s.csv' % (dataset_name, table_name, str(datetime.now()))
        write_csv_file(filename, data_fame)
        result = upload_file_to_bucket(filename, bucket_name)
    except IOError as error:
        return jsonify({'error': str(error)}), 500
    return jsonify({'response': result})