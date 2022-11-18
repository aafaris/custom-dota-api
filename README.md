# Custom OpenDota API

## Technologies Used
* Python 3.9.13
* Flask
* Postman
* Bootstrap 4
* Pycharm + Conda

## Installation
Please view the appropriate guide for conda before running the application in this repository.

Installing mandatory dependencies for the application in `requirements.txt` file
```bash
conda install --file requirements.txt
```
Now, the flask app is ready for use! To launch this application, execute this command:
```bash
python3 main.py
```
Alternatively, you can execute the command below:
```bash
set FLASK_RUN_PORT=PORT_NUMBER
set FLASK_APP=main.py
flask run
```
For more information about different execution environment, you can refer to Flask documentation: https://flask.palletsprojects.com/en/2.1.x/cli/

When using this application, you can expect such URLs upon user's request
```bash
localhost:5000/match/6842517916/all-time
localhost:5000/player/134784663
localhost:5000/match/6842517916/2022-11-15
```

## Two Primary Features

### 1. Rank Players in Match based on Win Rate (Period of Win Rate can be Varied)

### 2. Hero Recommendation based on Player's Historical Data
My recommendation engine takes into account of hero's win rate as well as the number of games played with that particular hero. If both of these attributes are high, it is high likely that would be your recommended hero and chances of winning the game is high. The recommendation are deduced in this following ratio:
```bash
ratio = (wins * wins) / (wins + losses)
```
The application will take the highest ratio as your recommended hero. This can be further enhanced through a thorough ranking procedure by using ELO rating algorithm where each hero holds its own rating based on their past games.

API calls are performed via asynchronous approach with `asyncio` and `aiohttp` modules where API calls are in event loop. Using general `requests` module will perform API calls synchronously instead. With `asyncio` and `aiohttp` modules, it speeds up API call performance, tackling limitations of calling multiple API calls. This allows me to retrieve leaderboard data and rendering of `leaderboard.html` faster, reducing waiting time from about 12 seconds to about 2 seconds for 10 API calls.
