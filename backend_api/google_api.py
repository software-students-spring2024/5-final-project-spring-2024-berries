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
    db = client["coffeedb"]
    cafesCollection = db["coffee"]
    print("Connected!")
except Exception as e:
    print(e)

#api_key = os.environ.get("GOOGLE_API_KEY")



@app.route("/find_cafes", methods=["POST"])
def find_cafes():
    data = request.get_json()
    latitude = data["latitude"]
    longitude = data["longitude"]
    

    #print("GOT RESUKTS!!!!")
    
    
    # api key and parameters for google places
    #api_key = os.getenv('GOOGLE_API_KEY')
    api_key = "AIzaSyC4jaf9Xb9_yFj-wl_hLJjL3CxXhGN1WfY"
    radius = 400  # ADJUSTABLE
    types = "cafe"  # search only cafes
    
    '''
    # if we want cafes with wifi
    keyword = "wifi"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={types}&keyword={keyword}&key={api_key}"
    '''
    # google api request
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={types}&key={api_key}"
    response = requests.get(url, timeout=15)

    if response.status_code == 200:
        # get info from api
        coffee_shops = []
        for place in response.json().get("results", []):
            # get a photo of coffeeshop
            photo_reference = (
                place["photos"][0]["photo_reference"]
                if "photos" in place and len(place["photos"]) > 0
                else None
            )

            coffee_shops.append(
                {
                    "name": place["name"],
                    "vicinity": place.get(
                        "vicinity"
                    ),  # vicinity = address in google places
                    "rating": place.get("rating"),
                    "photo_reference": photo_reference,
                }
            )

        return jsonify({"coffee_shops": coffee_shops})
    return (
        jsonify({"error": "Failed to fetch coffee shops from Google Places API."}),
        500,
    )
    




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)