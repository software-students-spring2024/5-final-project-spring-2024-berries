import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/coffee_shops')
"""
uri = "mongodb://mongodb:27017/"
    client = MongoClient(uri)
    db = client["cafes"]
    cafeDB = db["cafes"]
    print("Connected!")
"""

try:
    DB_USER = os.getenv("MONGODB_USER")
    DB_PASSWORD = os.getenv("MONGO_PWD")
    DB_HOST = os.getenv("DB_HOST")
    URI=f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}.5kr79yv.mongodb.net/"
    client = MongoClient(URI)
    db = client['cafes']
    gestureDB = db['cafes']
except Exception as e:
    print(e)



try:
    # verify the connection works by pinging the database
    client.admin.command("ping")  # The ping command is cheap and does not require auth.
    print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(" * ERRORRR", e)  # debug


@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")


# get users location and forward to machine learning model
@app.route("/find_coffee_shops", methods=["POST"])
def find_coffee_shops():
    """Get users location and forward to machine learning model."""
    data = request.get_json()

    # get long and lat
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return (
            jsonify({"error": "Latitude and longitude are required parameters."}),
            400,
        )

    # api key and parameters for google places
    api_key = "AIzaSyC4jaf9Xb9_yFj-wl_hLJjL3CxXhGN1WfY"
    radius = 400  # ADJUSTABLE
    types = "cafe"  # search only cafes

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


# show all results
@app.route("/results", methods=["POST"])
def show_results():
    """Show all results."""
    data = request.get_json()
    latitute = data["latitude"]
    longitude = data["longitude"]

    coffee_shops = db.cafes.find({"latitute": latitute, "longitude": longitude})

    shop_list = [shop for shop in coffee_shops]
    return render_template("results.html", coffee_shops=shop_list)


# ---------------------------------------------------------------------------- #
#                                     main                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5001")
    app.run(port=FLASK_PORT)
