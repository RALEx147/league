import re
from Game import Game
from bs4 import BeautifulSoup

def parse_aram_data(URL):
    page = open(URL)
    soup = BeautifulSoup(page.read(), features="html.parser")

    Final_List = []

    games = soup.find_all("div", "GameItemWrap")
    for i in games:
        winxxx = 0
        timexxx = 0
        championxxx = ""
        multikillxxx = ""
        maxlevelxxx = 0
        csxxx = 0
        csperminxxx = 0
        kpxxx = 0
        kdaxxx = 0
        team_namesxxx = []
        teamcompxxx = []
        itemsxxx = []

        output = i.find_all("div", "GameResult")
        for j in output:
            if "Victory" in str(j):
                winxxx = 1
            else:
                winxxx = 0

        output = i.find_all("div", "GameLength")
        for j in output:
            p = re.compile(r'.*?(\d+)m (\d+)s')
            m = p.match(str(j))
            if m is not None:
                minute = m.group(1)
                sec = m.group(2)
                timexxx = (int(minute) * 60) + int(sec)

        output = i.find_all("div", "ChampionName")
        for j in output:
            p = re.compile(r'.*\n.*>(.+)<\/a>\n.*')
            m = p.match(str(j))
            if m is not None:
                name = m.group(1)
                championxxx = name

        output = i.find_all("div", "MultiKill")
        for j in output:
            p = re.compile(r'.*\n.*>(\w+) Kill<\/span>\n.*')
            m = p.match(str(j))
            if m is not None:
                multikillxxx = m.group(1)


        output = i.find_all("div", "KDARatio")
        for j in output:
            p = re.compile(r'.*\n.*>(\d+.\d+):1.*')
            m = p.match(str(j))
            if m is not None:
                kdaxxx = m.group(1)

        output = i.find_all("div", "Level")
        for j in output:
            p = re.compile(r'.*\n.*Level(\d+).*\n.*')
            m = p.match(str(j))
            if m is not None:
                maxlevelxxx = m.group(1)

        output = i.find_all("div", "CS")
        for j in output:
            p = re.compile(r'.*\n.*>(\d+) \((\d*.\d*)\).*\n.*')
            m = p.match(str(j))
            if m is not None:
                csxxx = m.group(1)
                csperminxxx = m.group(2)

        output = i.find_all("div", "CKRate tip")
        for j in output:
            p = re.compile(r'.*\n.*?(\d+)%.*\n.*')
            m = p.match(str(j))
            if m is not None:
                kpxxx = m.group(1)

        output = i.find_all("div", "Team")
        team = []
        team_name = []
        opponents = []
        opponents_names = []
        counter = 0
        for j in output:
            if 'Summoner Requester' in str(j):
                inner = j.find_all("div", "ChampionImage")
                for o in inner:
                    p = re.compile(r'.*\n.*>(.*)<\/div>\n.*\n<\/div>')
                    m = p.match(str(o))
                    if m is not None:
                        team.append(m.group(1))
                inner = j.find_all("div", "SummonerName")
                for o in inner:
                    p = re.compile(r'.*\n.*>(.*)<\/a>.*\n<\/div>')
                    m = p.match(str(o))
                    if m is not None:
                        team_name.append(m.group(1))
            else:
                inner = j.find_all("div", "ChampionImage")
                for o in inner:
                    p = re.compile(r'.*\n.*>(.*)<\/div>\n.*\n<\/div>')
                    m = p.match(str(o))
                    if m is not None:
                        opponents.append(m.group(1))
                inner = j.find_all("div", "SummonerName")
                for o in inner:
                    p = re.compile(r'.*\n.*>(.*)<\/a>.*\n<\/div>')
                    m = p.match(str(o))
                    if m is not None:
                        opponents_names.append(m.group(1))
            counter += 1
            if counter % 2 == 0:
                teamcompxxx = (team, opponents)
                team_namesxxx = (team_name, opponents_names)
                team = []
                team_name = []
                opponents = []
                opponents_names = []

        output = i.find_all("div", "ItemList")
        for j in output:

            inner = j.find_all("div", "Item")

            for o in inner:
                # print(o)
                p = re.compile(r'.*\n<img alt="(.*?)" class=.*\n<\/div>')
                m = p.match(str(o))
                if m is not None:
                    itemsxxx.append(m.group(1))




        g = Game(winxxx, timexxx, championxxx, multikillxxx, maxlevelxxx, csxxx, csperminxxx, kpxxx, team_namesxxx, kdaxxx, teamcompxxx, itemsxxx)

        Final_List.append(g)
    return [x for x in Final_List if x.time != 0]
