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

@app.route('/api/v1/players', strict_slashes=False, methods=['GET'])
@app.route('/api/v1/players/<int:team_id>', strict_slashes=False, methods=['GET'])
def get_players(team_id: int = None):
    team = verify_token()

    if not team_id:
        team_id = team['id']

    team = {
        'team_id': team_id,
        'players': [p for p in mongo.db.players.find({'team_id': team_id})]
    }

    # cast id to string
    if team['players']:
        for player in team['players']:
            player['_id'] = str(player['_id'])
        
    return jsonify(team)

@app.route('/api/v1/player/<string:id>', strict_slashes=False, methods=['GET'])
def get_player(id: str):
    team = verify_token()
    try:
        objectId = ObjectId(id)
        player = mongo.db.players.find_one({'_id': objectId})
        player['_id'] = str(player['_id'])
    except InvalidId as err:
        abort(400, f'player id is not well formed: {str(err)}')
    except TypeError as err:
        abort(400, f'player "{str(objectId)}" does not exist')
    return jsonify(player)

@app.route('/api/v1/player', strict_slashes=False, methods=['POST'])
def post_player():
    team = verify_token()

    # we are forcing application/json
    raw_player = get_request_json_as_dict()

    # validate object is well-formed
    try:
        player = Player(**raw_player)
    except ValidationError as err:
        return jsonify(err.errors()), status.HTTP_400_BAD_REQUEST

    # set user id
    player.team_id = team['id']
    insert_result = mongo.db.players.insert_one(player.to_json())

    # set object id
    player_dict = player.to_json()
    player_dict['_id'] = str(insert_result.inserted_id)

    return jsonify(player_dict)


@app.route('/api/v1/player/<string:id>', strict_slashes=False, methods=['PUT'])
def put_player(id):
    team = verify_token()

    # we are forcing application/json
    raw_player = get_request_json_as_dict()

    # validate object is well-formed
    try:
        player = Player(**raw_player)

        # find the player
        objectId = ObjectId(id)
        player = mongo.db.players.find_one({'_id': objectId, 'team_id': player.team_id})

        # check the player exists
        assert player is not None

        # update
        mongo.db.players.update_one({'_id': objectId}, {"$set": raw_player})
        
        player["_id"] = str(player["_id"]) 
    except ValidationError as err:
        return jsonify(err.errors()), status.HTTP_400_BAD_REQUEST
    except InvalidId as err:
        abort(400, f'player id is not well formed: {str(err)}')
    except AssertionError as err:
        abort(400, f'player "{str(objectId)}" does not exist or you can not edit it')

    return jsonify(player)

@app.route('/api/v1/player/<string:id>', strict_slashes=False, methods=['DELETE'])
def delete_player(id):
    team = verify_token()
    try:
        objectId = ObjectId(id)
        player = mongo.db.players.find_one({'_id': objectId, 'team_id': team['id']})
        delete_result = mongo.db.players.delete_one({'_id': objectId, 'team_id': team['id']})
        player['_id'] = str(player['_id'])
    except InvalidId as err:
        abort(400, f'player id is not well formed: {str(err)}')
    except TypeError as err:
        abort(400, f'player "{str(objectId)}" does not exist or you can not delete it')
    return jsonify(player)

@app.route('/api/v1/notify-players/<int:team_id>', strict_slashes=False, methods=['POST'])
def notify_players(team_id):
    # we are forcing application/json
    raw_mail = get_request_json_as_dict()

    assert 'mail_sender'  in raw_mail, 'no "mail_sender" specified. Please, specify it.'
    assert 'mail_subject' in raw_mail, 'no "mail_subject" specified. Please, specify it.'
    assert 'mail_content' in raw_mail, 'no "mail_content" specified. Please, specify it.'

    team = {
        'team_id': team_id,
        'players': [p for p in mongo.db.players.find({'team_id': team_id})]
    }

    if not team['players']:
        abort(406, f'team "{team_id}" has zero players registered.')

    sendgrid_send_message(
        raw_mail['mail_sender'],
        [player['email'] for player in team['players']],
        raw_mail['mail_subject'],
        raw_mail['mail_content']
    )

    return make_response(f'mail sent successfully to {len(team["players"])} players (team_id = {team_id}).', 202)
