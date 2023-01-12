import json

from flask import request, abort


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
            return json.loads(request.data)
        except Exception as exc:
            abort(400, 'Request JSON data is ill-formed.')
    else:
        abort(400, 'Content-Type must be application/json.')