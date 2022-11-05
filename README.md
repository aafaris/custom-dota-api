# Healint Custom OpenDota API

## Technologies Used
* Python 3.9.13
* Flask
* Postman
* [Bootstrap 4](http://getbootstrap.com)

## Installation
Installing pip in conda environment
```bash
conda install pip
```
Once pip is installed, you can use it to install all python packages in the requirements.txt file
```bash
pip install -r requirements.txt
```
To launch flask app, execute this command:
```bash
set FLASK_RUN_PORT=8000
set FLASK_APP=hello.py
flask run
```
For more information, you can refer to Flask documentation: https://flask.palletsprojects.com/en/2.1.x/cli/

From the flask app, you can expect such URLs from user's request
```bash
localhost:5000/match/account-id/all-time
localhost:5000/player/134784663
http://localhost:5000/match/6842517916/2022-11-15
```

## Questions

### 1. Which tech stacks/frameworks did you consider for the development of this application?
Since I am required to develop this application via Python, I have considered three Python web frameworks, FastAPI, Django and Flask. Since I have working knowledge on Flask, I have decided to utilise the framework for this application development due to limited time given. This application was developed using Python Flask web framework coupled with Postman for my API development and Bootstrap 4 for my frontend development.

### 2. What are some limitations of your application and how do you plan to work around them in the future?
In this application, all data are retrieved from OpenDota directly. Hence, whenever such API calls failed to execute or when the internal server is down, this application will not be functional. In the future, I will integrate a database with this application to store data after executing API calls. This ensures that this application can continue running despite any server issues if the requested data exists. If the user requests for the same data, it can directly retrieve data from database instead of performing an API call. This will eventually boost the overall performance of this application especially when scaling. 

### 3. How would you ensure data required for the application stays up to date?
In this application, I have designed it in a way where it constantly perform API calls from OpenDota for every user's request. Hence, this ensures that the displayed results will always be up to date. However, this approach is rather expensive as performing API calls are costly and time consuming especially when dealing with high data volume.

### 4. Why is your recommendation engine a good solution?
In this application, I utilised `asyncio` and `aiohttp` modules for my API calls. Generally, API calls via Python are synchronous with `requests` module. However, with `asyncio` and `aiohttp` modules, I am able to perform my API calls via asynchronous approach where API calls are in an event loop. This approach speeds up the process of retrieving leaderboard data and rendering of `leaderboard.html`, reducing computational time from about 12 seconds to about 2 seconds for 10 API calls. Such process is optimal especially when requesting multiple API calls.

### 5. What are some features you would like to add to the application?
