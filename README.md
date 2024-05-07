[![CI for Backend](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/backend.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/backend.yml)
[![CI/CD for Web App](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/deployment.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/deployment.yml)
[![log github events](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/event-logger.yml)

# Final Project - Java Junction

## Overview 

The Java Junction web application utilizes the user's computer GPS to display cafes close in their area. Users will need to register and log into their account to start the application. After their session is connected and nearby cafes are displayed, users can leave a comment as a note under any cafe they choose. These comments will show up any time the user connects to the web application in the respective area. The user accounts and their respective comments are saved within a database.

## Features
* Cafe Locations: Displays cafes relative in location to user's computer GPS
* Comments: Designed to allow users to save comments that reflect their experiences with that cafe

## How to Run

Follow these steps to install and configure the necessary dependencies:

### 1. Clone the repo:
   ```bash
   git clone https://github.com/software-students-spring2024/5-final-project-spring-2024-berries.git
   cd 5-final-project-spring-2024-berries
   ```

### 2. Set up an .env at the root directory
```bash
MONGODB_USER="bcdy"
MONGO_PWD="your_mongodb_password"
DB_HOST="coffeeshops.5kr79yv.mongodb.net"
MONGO_DBNAME="coffeedb"
MONGO_COLLECTIONNAME="coffee"
API_KEY="your_google_api_key"
SECRET_KEY="your_secret_key_for_flask_session"
```
- Replace "your_mongodb_password" with your actual MongoDB password.
- Replace "your_google_api_key" with your actual Google API key.
- Replace "your_secret_key_for_flask_session" with a random string to secure Flask sessions.

### 3. Set up and run Docker application
- Make sure docker is running on your machine before entering this command:
```
docker-compose up --build
```
- After successful build, you can access the website at http://localhost:5001

## Container Images
- [web_app image](https://hub.docker.com/repository/docker/bonnychavarria/webapp/general)
- [backend_api image](https://hub.docker.com/repository/docker/bonnychavarria/webapp/general)

## Website
The website is deployed here: [Java Junction](http://45.55.200.164:5001)

Ensure the location setting is not blocked on your device!

## Contributors
* [Bonny](https://github.com/BonnyCChavarria) 
* [Christina](https://github.com/crb623)
* [Damla](https://github.com/damlaonder)
* [Yura](https://github.com/yurawu27)
