import os
import requests

import pytest


# test token
PLAYER_SERVICE = os.environ['PLAYER_SERVICE_URL']
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NjY0NjI1LCJpYXQiOjE2NzQxMjg2MjUsImp0aSI6IjQwZmNiN2IwZThjNjQwZDBiNzIwNzE3YmE0ZGE5YWQxIiwidXNlcl9pZCI6MTh9.JosnrKeXycoSFnj0CYE-429wDTJEGc8vkIrae8cPHy0"

def test_post():
    return True
