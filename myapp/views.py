from django.http import JsonResponse
from bson import ObjectId
import pymongo
from pymongo.server_api import ServerApi
from django.contrib.auth import authenticate, login

USERNAME = ""
PASSWORD = ""
CLUSTERURL = ""

uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTERURL}/?retryWrites=true&w=majority"

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))


def get_records(request):

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


def register(request):

    dbName = "Users"
    userCollections = "UserCollections"

    db = client[dbName]
    mycollection = db[userCollections]

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Add validation and error handling for form data here

        # Insert user data into MongoDB
        data = {
            'username': username,
            'email': email,
            'password': password
        }
        mycollection.insert_one(data)

        return JsonResponse({'data': 'success'})

    return JsonResponse({'data': 'failed'})
