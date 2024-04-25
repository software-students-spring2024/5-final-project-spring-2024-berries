import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from pymongo import MongoClient
import requests
import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#----- NEEDS TO CHANGE SECRET KEY -----#
app.secret_key = "323qssssa"

# app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/coffee_shops')
"""
uri = "mongodb://mongodb:27017/"
    client = MongoClient(uri)
    db = client["cafes"]
    cafeDB = db["cafes"]
    print("Connected!")
"""

try:
    '''
    DB_USER = os.getenv("MONGODB_USER")
    DB_PASSWORD = os.getenv("MONGO_PWD")
    DB_HOST = os.getenv("DB_HOST")
    URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}.5kr79yv.mongodb.net/"
    '''
    URI = "mongodb+srv://bcdy:BPoOlpuLgv3WKJ62@coffeeshops.5kr79yv.mongodb.net/"
    client = MongoClient(URI)
    db = client["coffeedb"]
    #cafesCollection = db["coffee"]
    user_collection = db["users"]
    
    # check if connected correctly
    print(URI)
    print("Connected!")
except Exception as e:
    print(e)

'''
try:
    # verify the connection works by pinging the database
    client.admin.command("ping")  # The ping command is cheap and does not require auth.
    print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(" * ERRORRR", e)  # debug
'''


@app.route('/register', methods=['POST', 'GET'])
def register():
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



# user login check
@app.route('/', methods=['POST', 'GET'])
def login():
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
    
   #  return redirect(url_for('home'))
    return render_template('log-in.html', message=message) 



# user logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



@app.route("/home")
def home():
    if 'username' not in session: # if user is not logged in
        return redirect(url_for('login'))
    
    return render_template("index.html")


@app.route("/find_coffee_shops", methods=["POST"])
def find_coffee_shops():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    api_url = "http://localhost:5002/find_cafes"  # URL to google_api.py service
    api_response = requests.post(api_url, json={"latitude": latitude, "longitude": longitude})
    if api_response.status_code == 200:
        return jsonify(api_response.json())
    else:
        return jsonify({"error": "Backend API failed"}), 500




'''
#---------------------THIS IS NEVER USED!!!----------------------------#
# show all results
@app.route("/results", methods=["POST"])
def show_results():
    """Show all results."""
    data = request.get_json()
    latitute = data["latitude"]
    longitude = data["longitude"]

    coffee_shops = cafesCollection.find({"latitute": latitute, "longitude": longitude})

    shop_list = [shop for shop in coffee_shops]
    return render_template("results.html", coffee_shops=shop_list)
'''


# ---------------------------------------------------------------------------- #
#                                     main                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5001")
    app.run(port=FLASK_PORT)
