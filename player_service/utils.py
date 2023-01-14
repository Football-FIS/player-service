import json
import os

import requests
import traceback

from flask import request, abort


VERIFY_TOKEN_URL = os.environ['VERIFY_TOKEN_URL']

####################################################################################################
# UTILS                                                                                            #
####################################################################################################

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
            traceback.print_exc()
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

    res = requests.get(VERIFY_TOKEN_URL, headers={"Authorization": authorization})

    if not res.ok:
        abort(401, res.text)
    else:
        return res.json()
