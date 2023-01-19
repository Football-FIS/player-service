import os
import requests

# test token
PLAYER_SERVICE = os.environ['PLAYER_SERVICE_URL']
AUTH_TOKEN = os.environ['AUTH_TOKEN']

# test data
PLAYER = {
    "_id": "",
    "email": "jose@email.com",
    "first_name": "jose",
    "last_name": "gonzalez",
    "position": "DELANTERO",
    "team_id": 0
}
HEADERS = {'Authorization': AUTH_TOKEN, 'Content-Type': 'application/json'}


def test_post():
    res = requests.post(PLAYER_SERVICE + '/api/v1/player', headers=HEADERS, json=PLAYER)
    assert res.status_code == 200, res.text
    global PLAYER_ID
    PLAYER_ID = res.json()['_id']

def test_get():
    res = requests.get(PLAYER_SERVICE + f'/api/v1/player/{PLAYER_ID}', headers=HEADERS)
    assert res.status_code == 200, PLAYER_ID

def test_put():
    res = requests.put(PLAYER_SERVICE + f'/api/v1/player/{PLAYER_ID}', headers=HEADERS, json=PLAYER)
    assert res.status_code == 200, res.text

def test_delete():
    res = requests.delete(PLAYER_SERVICE + f'/api/v1/player/{PLAYER_ID}', headers=HEADERS)
    assert res.status_code == 200, res.text

def test_players():
    res = requests.get(PLAYER_SERVICE + f'/api/v1/players/', headers=HEADERS)
    assert res.status_code == 200, res.text

def test_notify_players():
    match = {
        "alignment": "string",
        "city": "string",
        "id": "string",
        "is_local": True,
        "opponent": "string",
        "sent_email": True,
        "start_date": "string",
        "url": "string",
        "user_id": 0,
        "weather": "string"
    }

    res = requests.post(PLAYER_SERVICE + f'/api/v1/notify-players/', headers=HEADERS, json=match)
    assert res.status_code == 202, res.text
