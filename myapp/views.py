import os
from dotenv import load_dotenv, find_dotenv

from django.http import JsonResponse, HttpResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv(find_dotenv())

URI = os.environ['DB_URI']
DB_NAME = os.environ['DB_NAME']
COLL_NAME = os.environ['COLL_NAME']

client = MongoClient(URI, server_api=ServerApi('1'))


def home(request):
    content = '<p>There are thirty million songs on Spotify</p>' \
        '<p>Thirty million songs</p>' \
        '<p>Some are real big hits</p>' \
        '<p>Some are really... not</p>' \
        '<p>All songs are not created equal</p>' \
        '<p>Play the songs you love</p>' \
        '<p>Skip the ones you don\'t</p>' \
        '<p>Get a free thirty day trial of Premium</p>' \
        '<p>Skip whatever, we won\'t take it personally</p>' \
        '<p>So try premium, and start skipping</p>' \
        '<p>Tap the banner now to find out more</p>'

    return HttpResponse(content)


def get_records(request):
    try:
        db = client[DB_NAME]
        collection = db[COLL_NAME]
        records = collection.find()

        record_list = []

        for game in records:
            game['_id'] = str(game['_id'])
            record_list.append(game)

        return JsonResponse({'data': record_list})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
