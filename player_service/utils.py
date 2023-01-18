import json
import os

import requests
import traceback

from flask import request, make_response, abort as flask_abort

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


VERIFY_TOKEN_URL = os.environ['VERIFY_TOKEN_URL']

####################################################################################################
# UTILS                                                                                            #
####################################################################################################

def abort(status_code, message):
    """Abort and return error.
    """
    response = make_response(message, status_code)
    flask_abort(response)

def get_request_json_as_dict():
    """Returns request as a JSON. Content-Type must be application/json, otherwise 400 error will be
    thrown.
    """
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            body = json.loads(request.data)
            assert isinstance(body, dict)
            return body
        except:
            abort(400, 'Request body must be valid JSON data.')
    else:
        abort(400, 'Content-Type must be application/json.')


def verify_token():
    """Verify tokens from header Authorization.
    If an error is returned by TeamService, error 401 is thrown.
    If there is no Authorization on the header, error 400 is thrown.

    Returns:
        validate-token response as JSON.
    """
    # get token from header
    if "Authorization" in request.headers:
        authorization = request.headers.get('Authorization')
    else:
        abort(400, 'No "Authorization" on request header.')

    res = requests.get(VERIFY_TOKEN_URL, headers={"Authorization": authorization}, timeout=5)

    if not res.ok:
        abort(401, res.text)
    else:
        return res.json()

def sendgrid_send_message(from_email, to_emails, subject, content):
    """Send mail using sendgrid API.

    Args:
        from_email: sender email.
        to_e
        mails: list of receivers emails.
        subject: email subject.
        content: mail content.

    Raise:
        HTTPError: if the message could not be sent.
    """
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {os.environ.get("SENDGRID_API_KEY")}'
    }

    data = {
        "personalizations": [
            {
                "to": [{ "email": email } for email in to_emails],
                "subject": subject
            }
        ],
        "from": { "email": from_email },
        "content": [
            {
                "type": "text/plain",
                "value": content
            }
        ]}

    res = requests.post(os.environ.get('SENDGRID_URL'), headers=headers, data=json.dumps(data), timeout=5)

    if not res.ok:
        abort(res.status_code, res.text)

def create_mail_subject_from_match(match) -> str:
    """Given a match object return mail subject
    """
    return f"Match against {match.opponent} on {match.start_date}"

def create_mail_body_from_match(match) -> str:
    """Given a match object return mail body
    """
    return f"""Hi!.\n
You have a match scheduled:

\topponent:\t\t{match.opponent}
\tis_local:\t\t{match.is_local}
\talignment:\t\t{match.alignment}
\turl:\t\t{match.url}
\tcity:\t\t{match.city}
\tweather:\t\t{match.weather}
\tstart_date:\t\t{match.start_date}

Best regards!
"""