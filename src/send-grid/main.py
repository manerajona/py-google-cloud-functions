import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import functions_framework
import google.cloud.logging

# Instantiates Cloud Logging client
logging_client = google.cloud.logging.Client()
# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default, this captures all logs
# at INFO level and higher
logging_client.setup_logging()

sg = SendGridAPIClient(api_key='api-key')

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
        body = get_json_field(request_json, 'body')
        receiver_email = get_json_field(request_json, 'email')
    except ValueError as error:
        logging.warning(str(error))
        return str(error), 400

    # Construct the email message
    mail = Mail(
        from_email='manerajona@gmail.com',
        to_emails=receiver_email,
        subject=subject,
        html_content=body
    )

    logging.info("sending email...")
    # Send email using the Gmail API
    try:
        response = sg.send(mail)
        logging.info("response code: " + str(response))
        return str(response)
    except Exception as error:
        logging.error('An error occurred:' + str(error))
        return 500, f'An error occurred: {error}'
