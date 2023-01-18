import os

import funcy

from bson import ObjectId
from bson.errors import InvalidId

from pydantic import ValidationError

from flask import Flask, jsonify
from flask_api import status
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_caching import Cache
from flasgger import Swagger
from flask_cors import CORS, cross_origin

from model import Player, Match
from utils import *


app = Flask(__name__)

api = Api(app)

# set secret key from environment variable
app.secret_key = os.environ['SECRET_KEY']

# mongo db setting
app.config["MONGO_URI"] = os.environ['MONGO_URL']
mongo = PyMongo(app)

# Flask-Caching
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 60})
# cache.init_app(app)

# flasgger
swagger = Swagger(app)

# allow CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

####################################################################################################
# ENDPOINTS                                                                                        #
####################################################################################################

@app.route('/api/v1/players', strict_slashes=False, methods=['GET'])
@cross_origin()
def get_players():
    """Get list of players.
    ---
    definitions:
      Team:
        type: object
        properties:
          team_id:
            type: string
            required: true
          players:
            type: array
            items:
                $ref: '#/definitions/Player'
            required: true
    responses:
      200:
        description: A team object.
        schema:
          $ref: '#/definitions/Team'
      400:
        description: team_id ill-formed error or team_id doesn't exist error.      
    """
    team = verify_token()
    team = {
        'team_id': team['id'],
        'players': [p for p in mongo.db.players.find({'team_id': team['id']})]
    }

    # cast id to string
    if team['players']:
        for player in team['players']:
            player['_id'] = str(player['_id'])
        
    return jsonify(team)

@app.route('/api/v1/player/<string:id>', strict_slashes=False, methods=['GET'])
@cross_origin()
def get_player(id: str):
    """Get a player from player id.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    definitions:
      Player:
        type: object
        properties:
          _id:
            type: string
            required: true
          team_id:
            type: string
            required: true
          first_name:
            type: string
            required: true
          last_name:
            type: string
            required: true
          email:
            type: string
            required: true
          position:
            type: string
            required: true
    responses:
      200:
        description: A player object.
        schema:
          $ref: '#/definitions/Player'
      400:
        description: id ill-formed error or id doesn't exist error.
    """
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
@cross_origin()
def post_player():
    """Post a new player.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Player
    responses:
      200:
        description: A player object.
        schema:
          $ref: '#/definitions/Player'
      400:
        description: json body ill-formed.
    """
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
@cross_origin()
def put_player(id):
    """Modify a player.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Player
    responses:
      200:
        description: A player object.
        schema:
          $ref: '#/definitions/Player'
      400:
        description: json body ill-formed.      
    """
    team = verify_token()

    # we are forcing application/json
    raw_player = get_request_json_as_dict()

    # validate object is well-formed
    try:
        player = Player(**raw_player)

        # find the player
        objectId = ObjectId(id)
        update_result = mongo.db.players.update_one({'_id': objectId}, {"$set": funcy.omit(raw_player, ['_id', 'team_id'])})
    except ValidationError as err:
        return jsonify(err.errors()), status.HTTP_400_BAD_REQUEST
    except InvalidId as err:
        abort(400, f'player id is not well formed: {str(err)}')
    except AssertionError as err:
        abort(400, f'player "{str(objectId)}" does not exist or you can not edit it')

    return jsonify(raw_player)

@app.route('/api/v1/player/<string:id>', strict_slashes=False, methods=['DELETE'])
@cross_origin()
def delete_player(id):
    """Delete a player.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: Player
    responses:
      200:
        description: A player object.
        schema:
          $ref: '#/definitions/Player'
      400:
        description: id ill-formed error or id doesn't exist error.
    """
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

@app.route('/api/v1/notify-players', strict_slashes=False, methods=['POST'])
@cross_origin()
def notify_players():
    """Send messages to players.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Match
    definitions:
      Match:
        type: object
        properties:
          id:
            type: string
            required: true
          user_id:
            type: number
            required: true
          opponent:
            type: string
            required: true
          is_local:
            type: boolean
            required: true
          alignment:
            type: string
            required: true
          url:
            type: string
            required: true
          city:
            type: string
            required: true
          weather:
            type: string
            required: true
          start_date:
            type: string
            required: true
          sent_email:
            type: boolean
            required: true  
    responses:
      202:
        description: message indicating how many mails has been sent.
      400:
        description: team_id ill-formed error or team_id doesn't exist error.
    """
    # we are forcing application/json2
    raw_match = get_request_json_as_dict()

    try:
        match = Match(**raw_match)
    except ValidationError as err:
        return jsonify(err.errors()), status.HTTP_400_BAD_REQUEST

    mail_body = create_mail_body_from_match(match)
    mail_subject = create_mail_subject_from_match(match)

    team = {
        'team_id': match.user_id,
        'players': [p for p in mongo.db.players.find({'team_id': match.user_id})]
    }

    if not team['players'] or len(team['players']) == 0:
        return make_response(f'team "{match.user_id}" has zero players registered.', 202)

    sendgrid_send_message(
        os.environ['SENDGRID_SENDER_EMAIL'],
        set([player['email'] for player in team['players']]),
        mail_subject,
        mail_body
    )

    return make_response(f'mail sent successfully to {len(team["players"])} players (team_id = {match.user_id}).', 202)
