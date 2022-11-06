import requests
import asyncio
import aiohttp
import datetime
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if "m_id" in request.form:
            match_id = request.form["m_id"]
            timeframe = request.form["timeframe"]
            return redirect(url_for("match", match_id=match_id, t=timeframe))
        elif "custom_m_id" in request.form:
            match_id = request.form["custom_m_id"]
            timeframe = request.form["custom_date"]
            return redirect(url_for("match", match_id=match_id, t=timeframe))
        elif "p_id" in request.form:
            player_id = request.form["p_id"]
            return redirect(url_for("player", player_id=player_id))
    else:
        return render_template("index.html", template_folder="templates", sgt_dt=datetime.datetime.now())


@app.route("/match/<int:match_id>/<t>")
def match(match_id, t):
    data = get_leaderboard(match_id, t)
    return render_template("leaderboard.html", template_folder="templates", data=data)


@app.route("/player/<int:player_id>")
def player(player_id):
    hero, games, wins = get_recommended_hero(player_id)
    losses = games-wins
    win_rate = "{:.2%}".format(get_division(wins, games))
    return render_template("hero.html",
                           template_folder="templates",
                           player_id=player_id,
                           hero=hero,
                           games=games,
                           win_rate=win_rate,
                           wins=wins,
                           losses=losses)


def get_leaderboard(mid=None, t=None):
    res = requests.get(f"https://api.opendota.com/api/matches/{mid}")
    data = res.json()['players']

    period = {"last-week": 7, "last-month": 30, "three-month": 90, "six-month": 180, "twelve-month": 360}
    period_filter = False
    days = 0

    # determine period
    if t in period:
        days = period[t]
        period_filter = True
    else:
        if t == "all-time":
            pass
        else:
            days = get_days_difference(t)
            period_filter = True

    # async approach
    rankings, unknown_players = asyncio.run(get_async_leaderboard(data, period_filter, days))

    # rank according to highest win rate
    leaderboard = []
    leaderboard_keys = sorted(rankings, key=rankings.get, reverse=True)
    for k in leaderboard_keys:
        leaderboard.append((k, "{:.2%}".format(rankings[k])))

    # handle anonymous players
    if unknown_players > 0:
        leaderboard += (unknown_players*[("Anonymous", "N/A")])

    return leaderboard


def get_tasks(session, data, period_filter, days=0):
    tasks = []
    unknown_players = 0
    accounts = []
    for i in range(len(data)):
        account_id = data[i]['account_id']
        if account_id is None:
            unknown_players += 1
        else:
            if period_filter:
                tasks.append(session.get(f"https://api.opendota.com/api/players/{account_id}/wl?date={days}",
                                         ssl=False))
            else:
                tasks.append(session.get(f"https://api.opendota.com/api/players/{account_id}/wl",
                                         ssl=False))
            accounts.append(account_id)

    return tasks, accounts, unknown_players


async def get_async_leaderboard(data, period_filter, days=0):
    rankings = {}
    unknown_players = 0
    async with aiohttp.ClientSession() as session:
        tasks, accounts, unknown_players = get_tasks(session, data, period_filter, days)
        responses = await asyncio.gather(*tasks)
        for i, res in enumerate(responses):
            wl = await res.json()
            win_rate = get_division(wl['win'], wl['win']+wl['lose'])
            rankings[accounts[i]] = win_rate

    return rankings, unknown_players


def get_days_difference(date):
    current_date = datetime.datetime.strptime(datetime.date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    diff = current_date-datetime.datetime.strptime(date, "%Y-%m-%d")
    return diff.days


def get_division(num, denom):
    try:
        return num/denom
    except ZeroDivisionError:
        return 0


def get_recommended_hero(pid=None):
    res = requests.get(f"https://api.opendota.com/api/players/{pid}/heroes")
    data = res.json()

    # determine recommended hero - O(n) time complexity
    max_confidence = 0
    hero_id = None
    index = 0
    for i in range(len(data)):
        confidence_level = get_division(data[i]['win']*data[i]['win'], data[i]['games'])
        if confidence_level > max_confidence:
            max_confidence = max(max_confidence, confidence_level)
            hero_id = int(data[i]['hero_id'])
            index = i

    # retrieve hero name
    res = requests.get("https://api.opendota.com/api/heroes")
    for res in res.json():
        if res['id'] == hero_id:
            return res['localized_name'], data[index]['games'], data[index]['win']


if __name__ == '__main__':
    app.run()
