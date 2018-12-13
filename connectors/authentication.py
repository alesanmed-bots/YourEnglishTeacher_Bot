# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from configurations import bot_config
from . import mongo_connection as mongo

def auth_user(user, token):
    return_value = 1
    client = mongo.connect()

    db = client[bot_config.DB_NAME]

    token = db.auth_tokens.find_one({'token': token})

    if token and token['valid']:
        __authorize_user(user, db)
    else:
        return_value = 0
    
    mongo.close(client)

    return return_value

def check_authorization(user):
    authorized = 0
    client = mongo.connect()

    db = client[bot_config.DB_NAME]

    user = db.authorized_users.find_one({
        'user_id': user
    })

    if user and user['authorized']:
        authorized = 1
    
    mongo.close(client)

    return authorized

def __authorize_user(user, db):
    db.authorized_users.insert({
        'user_id': user,
        'authorized': 1,
    })
