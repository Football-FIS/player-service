import os

from flask import Flask, jsonify, abort

from flask_restful import Api
from flask_pymongo import PyMongo

from model import Player


app = Flask(__name__)

api = Api(app)

# set secret key from environment variable
app.secret_key = os.environ['SECRET_KEY']

app.config["MONGO_URI"] = os.environ['MONGO_URL']
mongo = PyMongo(app)

####################################################################################################
# ENDPOINTS                                                                                        #
####################################################################################################

@app.route('/api/v1/players/<string:team_id>', methods=['GET'])
def get_players(team_id: str):
    team = {
        'team_id': team_id,
        'players': [p for p in mongo.db.players.find({'team_id': team_id})]
    }

    if not team['players']:
        abort(400, f'there are no players for team "{str(team_id)}"')

    # cast id to strong
    for player in team['players']:
        player['_id'] = str(player['_id'])
        
    return jsonify(team)
