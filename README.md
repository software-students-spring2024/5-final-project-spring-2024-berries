![backend](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/backend.yml/badge.svg)
![deployment](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/deployment.yml/badge.svg)
![event-logger](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/event-logger.yml/badge.svg)

# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## Installation

Follow these steps to install and configure the necessary dependencies:

### 1. Clone the repo:
   ```bash
   git clone https://github.com/software-students-spring2024/5-final-project-spring-2024-berries_.git
   cd 5-final-project-spring-2024-berries
   ```

### 2. Install python

To run this project, you will need Python 3.10.
    
1. Visit the official Python website at [python.org](https://www.python.org/downloads/).
2. Download the appropriate installer for your operating system. Make sure to select "Add Python to PATH" before installing (important for Windows users).
3. Follow the installation instructions to install Python on your system.


### 3. Create a virtual environment

Navigate to your project's directory in the command line, then run:
```bash
python -m venv venv
```
On macOS and Linux:
```bash
source venv/bin/activate
```
On Windows:
```bash
.\venv\Scripts\activate
```

### 4. Install dependencies:
```bash
python -m pip install --upgrade pip
pip install -r web_app/requirements.txt
```
### 5. Run app:

### 6. Build Docker Images:

## Container Images
[web_app image](https://hub.docker.com/repository/docker/bonnychavarria/webapp/general)
[backend_api image](https://hub.docker.com/repository/docker/bonnychavarria/backend_api/general)

## Contributors
* [Bonny](https://github.com/BonnyCChavarria) 
* [Christina](https://github.com/crb623)
* [Damla](https://github.com/damlaonder)
* [Yura](https://github.com/yurawu27)
