from bs4 import BeautifulSoup as bs
import requests, json, random
import numpy as np
from matplotlib import pyplot as plt

# page = requests.get("https://kenpom.com/index.php")
# page = bs(page.text)
#
# table = page.find("table", id = "ratings-table")
# body = table.find("tbody")
# line = body.find_all("tr")
#
# b = {}
# b['teams'] = []
# for x in line:
#     try:
#         name = x.find_all('a')[0].text
#         conference = x.find_all('a')[1].text
#         elo = 1500 + (float(x.find_all('td')[4].text)*7)
#         b['teams'].append([name, conference, elo])
#     except:
#         pass
#
# print(b['teams'])
#
# with open("teams.json", "w+") as file:
#     json.dump(b, file)

with open("teams.json", "r") as file:
    data = json.load(file)

teams = {}
teams['teams'] = []

history = {}
history['teams'] = []

for x in data['teams']:
    team = {
        "name": x[0],
        "elo": x[2],
        "conference": x[1],
        "win": 0,
        "loss":0,
        'originalelo': x[2]
    }
    teams['teams'].append(team)
    team = {
        'name': x[0],
        "rankings": []
    }
    history['teams'].append(team)

def season():
    def play(home, away):
        homeelo = home['elo']
        awayelo = away['elo']
        homewin = (1 / (10 ** (-(homeelo-awayelo) / 400) + 1))*100
        num = random.randint(0, 100)
        if num <= homewin:
            home['elo'] = homeelo + (32 * (1 - (homewin/100)))
            away['elo'] = awayelo + (32 * (0 - (1-(homewin/100))))
            home['win'] = home['win'] + 1
            away['loss'] = away['loss'] + 1
        else:
            home['elo'] = homeelo + (32 * (0 - (1-(homewin/100))))
            away['elo'] = awayelo + (32 * (1 - (1 - (homewin/100))))
            away['win'] = away['win'] + 1
            home['loss'] = home['loss'] + 1
        return(home, away)

    def conference():
        global teams
        for x in range(len(teams['teams'])):
            home = teams['teams'][x]
            for y in range(x+1, 356):
                away = teams['teams'][y]
                if home['conference'] == away['conference']:
                    # print(home['name'], away['name'])
                    teams['teams'][x], teams['teams'][y] = play(home, away)

    def nonconference():
        global teams
        for x in range(len(teams['teams'])):
            home = teams['teams'][x]
            gamesplayed = 30-(int(home['win'])+int(home['loss']))
            for y in range(gamesplayed):
                count = 0
                while True:
                    num = random.randint(0, len(teams['teams'])-1)
                    away = teams['teams'][num]
                    if away['conference'] != home['conference']:
                        if int(int(away['win'])+int(away['loss'])) < 30:
                            if home['conference'] != away['conference']:
                                break
                        else:
                            count += 1
                    if count >= 100:
                        break

                teams['teams'][x], teams['teams'][num] = play(home, away)

    conference()
    nonconference()
    ranking = sorted(teams['teams'], key = lambda i: i['elo'], reverse=True)
    count = 1
    for x in range(0, 356):
        # print(ranking[x]['name'], ranking[x]['elo'], count)
        for y in history['teams']:
            if y['name'] == ranking[x]['name']:
                y['rankings'].append(count)
        count += 1

    for x in ranking:
        elo = x['elo']
        leaving = elo*0.2
        elo = int(elo-leaving) + int(np.random.normal(leaving, 2, 1)[0])
        x['elo'] = elo

for x in range(0, 100):
    season()

with open("1000.json", "w") as file:
    json.dump(history, file)

while True:
    team = input("Team: ")
    for x in history['teams']:
        if x['name'] == team:
            plt.plot(x['rankings'])
            plt.show()
