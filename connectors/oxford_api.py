# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from configurations import bot_config
import requests

def get_word_definition(word):
    APP_ID = bot_config.OXFORD_API_ID
    API_KEY = bot_config.OXFORD_API_KEY

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/%s' % (word.lower(),)

    return requests.get(url, headers={'app_id': APP_ID, 'app_key': API_KEY})


if __name__ == '__main__':
    print(get_word_definition('table').json())