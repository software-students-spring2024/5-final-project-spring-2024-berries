[![CI for Backend](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/backend.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/backend.yml)
[![CI/CD for Web App](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/deployment.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/deployment.yml)
[![log github events](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-berries/actions/workflows/event-logger.yml)

# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

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
- [backend_api image](https://hub.docker.com/repository/docker/bonnychavarria/backend_api/general)

## Contributors
* [Bonny](https://github.com/BonnyCChavarria) 
* [Christina](https://github.com/crb623)
* [Damla](https://github.com/damlaonder)
* [Yura](https://github.com/yurawu27)
