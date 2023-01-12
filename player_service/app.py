import os

from flask import Flask, jsonify, abort

from bson import ObjectId
from bson.errors import InvalidId

from pydantic import ValidationError

from flask_api import status
from flask_restful import Api
from flask_pymongo import PyMongo

from model import Player
from utils import *


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

    # cast id to string
    for player in team['players']:
        player['_id'] = str(player['_id'])
        
    return jsonify(team)

@app.route('/api/v1/player/<string:id>', methods=['GET'])
def get_player(id: str):
    try:
        objectId = ObjectId(id)
        player = mongo.db.players.find_one({'_id': objectId})
        player['_id'] = str(player['_id'])
    except InvalidId as err:
        abort(400, f'player id is not well formed: {str(err)}')
    except TypeError as err:
        abort(400, f'player "{str(objectId)}" does not exist')
    return jsonify(player)

@app.route('/api/v1/player', methods=['POST'])
def post_player():
    # we are forcing application/json
    raw_player = get_request_json_as_dict()

    # validate object is well-formed
    try:
        player = Player(**raw_player)
    except ValidationError as err:
        return jsonify(err.errors()), status.HTTP_400_BAD_REQUEST

    insert_result = mongo.db.players.insert_one(player.to_json())

    # set object id
    player_dict = player.to_json()
    player_dict['_id'] = str(insert_result.inserted_id)

    return jsonify(player_dict)


@app.route('/api/v1/player', methods=['PUT'])
def put_player():
    # we are forcing application/json
    raw_player = get_request_json_as_dict()

    try:
        _id = raw_player.pop('_id')
    except:
        abort(400, 'no field "_id" in body json.')

    # validate object is well-formed
    try:
        player = Player(**raw_player)
        mongo.db.players.update_one({'_id': ObjectId(_id)}, {"$set": player.to_json()})
    except ValidationError as err:
        return jsonify(err.errors()), status.HTTP_400_BAD_REQUEST
    except InvalidId as err:
        abort(400, f'player id is not well formed: {str(err)}')

    return jsonify(raw_player)