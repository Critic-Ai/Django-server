import os
from dotenv import load_dotenv, find_dotenv

from django.http import JsonResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv(find_dotenv())

URI = os.environ['DB_URI']

client = MongoClient(URI, server_api=ServerApi('1'))


def get_records(request):
    # return JsonResponse({'url': URI}) # works

    dbName = "Ratings"
    RatingCollections = "RatingCollections"

    db = client[dbName]
    mycollection = db[RatingCollections]
    records = mycollection.find()

    record_list = []
    for record in records:
        record['_id'] = str(record['_id'])  # Convert ObjectId to string
        record_list.append(record)

    return JsonResponse({'data': record_list})
