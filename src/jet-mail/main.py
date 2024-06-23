import logging

import functions_framework
import google.cloud.logging
from flask import jsonify
from mailjet_rest import Client

# Instantiates Cloud Logging client
logging_client = google.cloud.logging.Client()
# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default, this captures all logs
# at INFO level and higher
logging_client.setup_logging()

# Mailjet API credentials
MAILJET_API_KEY = 'api-key'
MAILJET_API_SECRET = 'secret'


def get_json_field(request_json, field_name):
    if request_json and field_name in request_json:
        return request_json[field_name]
    else:
        raise ValueError('JSON is invalid, or missing a "' + field_name + '" property')


@functions_framework.http
def send_email(request):
    request_json = request.get_json(silent=True)
    # set variables from request Json
    try:
        subject = get_json_field(request_json, 'subject')
        message = get_json_field(request_json, 'body')
        recipient = get_json_field(request_json, 'email')
    except ValueError as error:
        logging.warning(str(error))
        return jsonify({'error': error}), 400

    # Initialize Mailjet client
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')

    # Prepare email message
    data = {
        'Messages': [
            {
                'From': {
                    'Email': 'manerajona@gmail.com',
                    'Name': 'O&I Notification'
                },
                'To': [
                    {
                        'Email': recipient,
                    }
                ],
                'Subject': subject,
                'TextPart': message
            }
        ]
    }

    try:
        # Send email via Mailjet API
        response = mailjet.send.create(data=data)
        logging.info("response: " + str(response))
        return jsonify({'response': response.json()}), 200
    except Exception as e:
        logging.error('An error occurred:' + str(e))
        return jsonify({'error': str(e)}), 500