import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from pymongo import MongoClient
import requests
import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = "323qssssa"

try:
    URI = "mongodb+srv://bcdy:BPoOlpuLgv3WKJ62@coffeeshops.5kr79yv.mongodb.net/"
    client = MongoClient(URI)
    db = client["coffeedb"]
    user_collection = db["users"]
    # check if connected correctly
    # print(URI)
    #print("Connected!")
except Exception as error:
    print(error)


try:
    # verify the connection works by pinging the database
    client.admin.command("ping")  # The ping command is cheap and does not require auth.
    print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
except Exception as err:
    # the ping command failed, so the connection is not available.
    print(" * ERRORRR", err)  # debug


@app.route('/register', methods=['POST', 'GET'])
def register():
    """
    Registers a new user by adding the user's name, username, and password to the database.

    Returns:
        HTML: The sign-up page if the user is not logged in, else the home page.
    """
    message = None
    if request.method == 'POST':
        new_name = request.form['name']
        new_username = request.form['username']
        new_password = request.form['password']

        existing_user = user_collection.find_one({'username': new_username})
        #existing_user = user_collection.find({})
        #print(existing_user)

        if existing_user is None:
            #hashpass = bcrypt.hashpw(new_password, bcrypt.gensalt())
            hashpass = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user_collection.insert_one({'username': new_username, 'password': hashpass, 'name': new_name})
            session['username'] = new_username
            return redirect(url_for('home'))

        message = 'That username already exists!'
        return render_template('sign-up.html', message=message)

    return render_template('sign-up.html', message=message)


@app.route('/', methods=['POST', 'GET'])
def login():
    """
    Logs in the user by checking the username and password in the database.

    Returns:
        HTML: The login page if the user is not logged in, else the home page.
    """
    message = None
    if request.method == 'POST':
        login_user = user_collection.find_one({'username': request.form['username']})
        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('home'))
        else:
            message = 'User not found! Please register first.'
            # return redirect(url_for('log-in'))
            return render_template('log-in.html', message=message)

        message = 'Wrong username or password. Please try again.'
        return render_template('log-in.html', message=message)
        # return redirect(url_for('login'))

    # return redirect(url_for('home'))
    return render_template('log-in.html', message=message)


@app.route('/logout')
def logout():
    """
    Logs out the user by removing the 'username' key from the session.

    Returns:
        Redirect: Redirects to the login page.
    """
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/home")
def home():
    """
    Renders the home page if the user is logged in, else redirects to the login page.

    Returns:
        HTML: The home page if the user is logged in, else the login page.     
    """
    if 'username' not in session: # if user is not logged in
        return redirect(url_for('login'))

    return render_template("index.html")


@app.route('/get_comments', methods=['GET'])
def get_comments():
    """
    Gets the comments for the coffee shop with the specified ID.

    Returns:
        the comments as a JSON object.
    """
    if 'username' not in session:
        return redirect(url_for('login'))

    coffee_shop_id = request.args.get('coffee_shop_id')
    user = user_collection.find_one({'username': session['username']})
    comments = [c for c in user.get('comments', []) if c['coffee_shop_id'] == coffee_shop_id]
    return jsonify({"comments": [c['comment'] for c in comments]})


@app.route('/add_comment', methods=['POST'])
def add_comment():
    """
    Adds a comment to the user's profile.

    Returns:
        JSON: A JSON object with the status of the comment addition.
    """
    if 'username' not in session:
        return redirect(url_for('login'))

    user = user_collection.find_one({'username': session['username']})
    comment_data = request.get_json()
    coffee_shop_id = comment_data['coffee_shop_id']
    comment = comment_data['comment']
    # Append comment
    user_collection.update_one(
        {'_id': user['_id']},
        {'$push': {'comments': {'coffee_shop_id': coffee_shop_id, 'comment': comment}}}
    )
    return jsonify({"status": "success"})


@app.route("/find_coffee_shops", methods=["POST"])
def find_coffee_shops():
    """
    Finds coffee shops near the specified latitude and longitude.

    Expects JSON data with keys 'latitude' and 'longitude'.
    Makes a request to an external service (method in backend_api) to find cafes based on the provided latitude and longitude.

    Returns:
        JSON: A list of coffee shops found near the specified latitude and longitude.

    Raises:
        HTTPError: If the request to the external service fails.
    """
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    api_url = "http://localhost:5002/find_cafes"  # URL to google_api.py service
    try:
        api_response = requests.post(api_url, json={"latitude": latitude, "longitude": longitude}, timeout=10)
        api_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch coffee shops from Google Places API: {e}"}), 500

    return jsonify(api_response.json())



if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5001")
    app.run(port=FLASK_PORT)
