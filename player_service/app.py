#!/usr/bin/env python
# encoding: utf-8

import os

from flask import Flask


app = Flask(__name__)

# set secret key from environment variable
app.secret_key = os.environ['SECRET_KEY']

@app.route('/hello', methods=['GET'])
def delete_player(id):
    return "hello-from-flask"
