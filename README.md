# Healint Custom OpenDota API

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

## Questions & Answers
### 1. Which tech stacks/frameworks did you consider for the development of this application?
Since I am required to develop this application via Python, I have considered three Python web frameworks, FastAPI, Django and Flask. Due to limited time given, I have decided to develop this application with Flask as I have working knowledge on Flask than the other two frameworks, allowing me to deliver this application effectively. Furthermore, Flask promotes rapid development and flexibility which I believe is sufficient to satisfy the requirements of this application. This application was developed via Python Flask web framework coupled with Postman for my API development and Bootstrap 4 for my frontend development.

### 2. What are some limitations of your application and how do you plan to work around them in the future?
In this application, all data are retrieved from OpenDota directly. Hence, whenever the internal server is down, this application will not be functional. In the future, I will integrate a database with this application to store data after executing API calls. This ensures that this application can continue running despite any server issues if the requested data exists. If the user requests for the same data, it can directly retrieve data from the database instead of performing another API call. This will eventually boost the overall performance of this application especially when scaling. Timestamp will be stored as one of the attributes in the database. The timestamp will act as an identifier to represent freshness of data. For instance, if a particular data exceeds 7 days from current date, it will prompt a new API call and present new data to the user while updating the new data in the database.

### 3. How would you ensure data required for the application stays up to date?
In this application, I have designed it in such a way that it constantly performs API calls from OpenDota for every user's request. Hence, this ensures that the displayed results will always be up to date. However, this approach is rather expensive as performing API calls frequently are costly and time consuming especially when dealing with high data volume. Moving forward, this can be further improved by integrating a database into this application.

### 4. Why is your recommendation engine a good solution?
My recommendation engine takes into account of hero's win rate as well as the number of games played with that particular hero. If both of these attributes are high, it is high likely that would be your recommended hero and chances of winning the game is high. The recommendation are deduced in this following ratio:
```bash
ratio = (wins * wins) / (wins + losses)
```
The application will take the highest ratio as your recommended hero. However, I believe that such recommendation can be further enhanced through a thorough ranking procedure by using ELO rating algorithm where each hero holds its own rating based on their past games.

In addition, I performed my API calls via asynchronous approach with `asyncio` and `aiohttp` modules. Generally, API calls via Python are synchronous with `requests` module. However, with `asyncio` and `aiohttp` modules, I am able to perform my API calls much effectively where API calls are in an event loop. This speeds up my API call performance, tackling limitations of calling multiple API calls. This allows me to retrieve leaderboard data and rendering of `leaderboard.html` faster, reducing waiting time from about 12 seconds to about 2 seconds for 10 API calls. I believe such enhancements are important especially when requesting multiple API calls.

### 5. What are some features you would like to add to the application?
- Alert players on their gameplay performance by using player's playing style data such as gold per min and last hits. This can be used as an indicator for players whether they are underperforming or outperforming by getting their average from their previous gameplay and which aspects of attributes they should focused on for a higher chance of winning future games.
- Suggest a hero for players in a 5 vs 5 team setting such as Support, Carry etc; suggesting which hero complements with each other in a team.
