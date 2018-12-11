# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from configurations import bot_config
from . import mongo_connection as mongo
import datetime

def insert_word(word):
    client = mongo.connect()

    db = client[bot_config.DB_NAME]

    word['fetched'] = 0

    inserted_id = db.words.insert_one(word).inserted_id

    mongo.close(client)

    return inserted_id

def get_daily_word():
    client = mongo.connect()

    db = client[bot_config.DB_NAME]

    if db.words.count_documents({'fetched': 0}) == 0:
        db.words.update_many({}, {'$set': {'fetched': 0}})

    aggregation_pipeline = [
        {'$match': {'fetched': 0}},
        {'$sample': {'size': 1}}
    ]

    random_word = list(db.words.aggregate(aggregation_pipeline))[0]

    db.words.update_one({'_id': random_word['_id']}, {'$set': {'fetched': 1}})

    mongo.close(client)

    return random_word

def get_first_word():
    client = mongo.connect()

    db = client[bot_config.DB_NAME]

    aggregation_criteria = 1

    if db.words.count_documents({'fetched': 1}) == 0:
        aggregation_criteria = 0

    aggregation_pipeline = [
        {'$match': {'fetched': aggregation_criteria}},
        {'$sample': {'size': 1}}
    ]

    random_word = list(db.words.aggregate(aggregation_pipeline))[0]

    mongo.close(client)

    return random_word

def check_duplicate_word(word):
    client = mongo.connect()

    db = client[bot_config.DB_NAME]

    duplicate = db.words.count_documents({
        'word': {
            '$regex': word,
            '$options': 'i'
        }
    })

    mongo.close(client)

    return duplicate

def insert_suggestion(suggestion):
    client = mongo.connect()

    db = client[bot_config.DB_NAME]

    suggestion['added'] = datetime.datetime.now()

    inserted_id = db.suggestions.insert_one(suggestion).inserted_id

    mongo.close(client)

    return inserted_id
