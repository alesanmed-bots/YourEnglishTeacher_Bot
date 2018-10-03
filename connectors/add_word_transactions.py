# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from configurations import bot_config
from . import mongo_connection as mongo

def insert_word(word):
    client = mongo.connect()

    db = client[bot_config.DB_NAME]

    word['fetched'] = 0

    inserted_id = db.words.insert_one(word).inserted_id

    mongo.close(client)

    return inserted_id
