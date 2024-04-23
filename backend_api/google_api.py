import os
from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)


"""try:
    uri = "mongodb://mongodb:27017/"
    client = MongoClient(uri)
    db = client["cafes"]
    cafesCollection = db["cafes"]
    print("Connected!")

except Exception as e:
    print(e)"""

try:
    DB_USER = os.getenv("MONGODB_USER")
    DB_PASSWORD = os.getenv("MONGO_PWD")
    DB_HOST = os.getenv("DB_HOST")
    URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}.5kr79yv.mongodb.net/"
    client = MongoClient(URI)
    db = client["cafes"]
    cafesCollection = db["cafes"]
    print("Connected!")
except Exception as e:
    print(e)


api_key = os.environ.get("GOOGLE_API_KEY")


@app.route("/find_cafes", methods=["POST"])
def find_cafes():
    """Get cafe information from Google Places API"""
    data = request.get_json()
    latitude = data["latitude"]
    longitude = data["longitude"]

    # google_api_key = "AIzaSyC4jaf9Xb9_yFj-wl_hLJjL3CxXhGN1WfY"  # google api
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1000&type=cafe&key={api_key}"
    response = requests.get(places_url, timeout=15)
    results = response.json().get("results", [])

    # cafe data -> mongo db
    # pull stats from json
    # insert into collection
    for cafe in results:
        cafe_data = {
            "name": cafe.get("name"),
            "location": cafe["geometry"]["location"],
            "vicinity": cafe.get("vicinity"),
            "rating": cafe.get("rating"),
            "user_ratings_total": cafe.get("user_ratings_total"),
        }
        cafesCollection.insert_one(cafe_data)

    # basic info - name and location of cafe
    simplified_results = [
        {"name": cafe.get("name"), "address": cafe.get("vicinity")} for cafe in results
    ]

    return jsonify(simplified_results)


if __name__ == "_main_":
    app.run(debug=True, port=5002)