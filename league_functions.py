import os
import time
from collections import defaultdict, namedtuple
import dill
import numpy
from league_constants import adcs
from Game import Match, Summoner, Stats
import cassiopeia as cass


def pretty(d, length):
    for key, value in d:
        space = " " * (length - len(key))
        print(str(key)+space+str(value))

def load_data(name):
    Aram_Data = dill.load(open("data_"+ name.lower().replace(" ", "_")+".pickle", "rb"))
    read_set = dill.load(open("read_"+ name.lower().replace(" ", "_")+".pickle", "rb"))
    print("DATA LOADED",len(Aram_Data))
    return Aram_Data, read_set


def fetch_new_data(read, matches, name):
    last_updated = 0
    try:
        last_updated = os.stat("data_"+ name.replace(" ", "_")+".pickle").st_mtime
    except:
        pass
    if time.time() - last_updated > 3600:
        settings = {"logging": {"print_calls": False}}
        cass.apply_settings(settings)
        cass.set_riot_api_key("***REMOVED***")

        summoner = cass.get_summoner(name=name, region="NA")
        queue = [cass.Queue.aram]
        Player = namedtuple('Player', ['name', 'champ'])
        champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region="NA")}
        summonerspell_id_to_name_mapping = {spell.id: spell.name for spell in cass.get_summoner_spells(region="NA")}

        print("Getting Match History")
        match_history = cass.get_match_history(summoner=summoner, queues=queue)
        print("Total Games:", len(match_history))
        match_history = list(filter(lambda x: x.id not in read, match_history))
        print("NEW Games:", len(match_history))
        print("Getting Game Data")

        count = 0
        for match in match_history:
            if count % 100 == 0 and count > 0:
                print(round(count * 100 / len(match_history)), '/ 100')
                # dill.dump(matches, file = open("Aram_Data_Checkpoint.pickle", "wb"))
                # dill.dump(read, file = open("Read_Checkpoint.pickle", "wb"))
            blue = []
            red = []
            main_summoner = None
            side = None

            for i in match.participants:
                if i.side.value == 100:
                    blue.append(Player(i.summoner.name, i.champion.name))
                else:
                    red.append(Player(i.summoner.name, i.champion.name))

                if i.summoner == summoner:
                    side = 0 if i.side.value == 100 else 1
                    champion = champion_id_to_name_mapping[i.champion.id]
                    summoner_spell_d = summonerspell_id_to_name_mapping[i.summoner_spell_d.id]
                    summoner_spell_f = summonerspell_id_to_name_mapping[i.summoner_spell_f.id]
                    runes = {r.name for r in i.runes}
                    try:
                        stats = Stats(i.stats)
                    except:
                        stats = i.stats
                    main_summoner = Summoner(summoner_spell_d, summoner_spell_f, runes, stats)

            game = Match(match.duration, match.season, match.patch, match.id, blue, red, main_summoner, side)
            matches.append(game)
            read.add(match.id)
            count += 1

        print("DATA ADDED", count, '\n')

        dill.dump(matches, file = open("data_"+ name.replace(" ", "_")+".pickle", "wb"))
        dill.dump(read, file = open("read_"+ name.replace(" ", "_")+".pickle", "wb"))
    else:
        print("NO DATA ADDED\n")
    return matches



# def win_rate(name, data):
# def champ_winrate(name, data):
# def champ_kda(name, data):
# def kda(data):
# def kp(data):
# def common_teammates(data, lookup=None):
# def multikills(data):
# def items(data):
# def adc_winrate(data):
# def time_played(data):
# def win_rate_with(name, data):
def time_distribution(name, data):
    winlength = defaultdict(int)
    loselength = defaultdict(int)

    win_times = []
    loss_times = []
    for i in data:
        if name in i.team_names[0]:
            t = int(i.time / 60)
            if i.win:
                winlength[t] += 1
                win_times.append(i.time)
            else:
                loselength[t] += 1
                loss_times.append(i.time)

    wins = sorted(winlength.items(), key=lambda item: item[0])
    loss = sorted(loselength.items(), key=lambda item: item[0])


    print("Wins")
    for i, val in enumerate(wins):
        print(str(val[0])+"*"*val[1])
    print('-------------------------------')

    print("Losses")
    for i, val in enumerate(loss):
        print(str(val[0])+"*"*val[1])


    win_mean = sum(win_times)/len(win_times)
    loss_mean = sum(loss_times)/len(loss_times)
    total_count = len(win_times) + len(loss_times)
    total_time = win_times + loss_times
    print("Average Win Time ", win_mean/60)
    print("Average Loss Time ", loss_mean/60)
    print("Average Time", sum(total_time) /60/total_count)
    print("Win Standerd Deviation", (numpy.std(win_times))/60)
    print("Loss Standerd Deviation", (numpy.std(loss_times))/60)
    print("Standerd Deviation",(numpy.std(win_times + loss_times))/60)
    print()
