import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#api_key = os.environ.get("GOOGLE_API_KEY")


@app.route("/find_cafes", methods=["POST"])
def find_cafes():
    """
    Finds cafes based on latitude and longitude.

    Expects JSON data with keys 'latitude' and 'longitude'.
    Returns JSON response with a list of cafes found.

    Returns:
        JSON: A list of cafes found near the given latitude and longitude.
    """
    data = request.get_json()
    latitude = data["latitude"]
    longitude = data["longitude"]

    # api key and parameters for google places
    #api_key = os.getenv('GOOGLE_API_KEY')
    api_key = os.getenv("API_KEY")
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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
