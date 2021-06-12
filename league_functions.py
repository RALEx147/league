import os
from collections import defaultdict, namedtuple
import dill
import numpy
from league_parser import parse_aram_data
from league_constants import adcs
from Game import Match, Summoner, Stats
import cassiopeia as cass


def pretty(d, length):
    for key, value in d:
        space = " " * (length - len(key))
        print(str(key)+space+str(value))


def load_data_old(string, set_name):
    Aram_Data = dill.load(open(string, "rb"))
    read_set = dill.load(open(set_name, "rb"))
    print("DATA LOADED",len(Aram_Data))
    return Aram_Data, read_set


def fetch_new_data_old(read_set, data):
    data_size = len(data)
    Aram_Data = data

    for i in [x for x in os.listdir("aram_data") if x.split(".")[-1] == 'htm']:
        if i not in read_set:
            URL = '/Users/rale/Documents/Programming/league/aram_data/' + i
            New_Aram_Data = parse_aram_data(URL)
            Aram_Data = New_Aram_Data + Aram_Data
            read_set.add(i)
    dill.dump(Aram_Data, file = open("Aram_Data.pickle", "wb"))
    dill.dump(read_set, file = open("read_set.pickle", "wb"))
    print("DATA ADDED", len(Aram_Data) - data_size, '\n')


    return Aram_Data

def fetch_new_data(read, matches, name):
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
    print("Total Aram Games:", len(match_history))
    match_history = list(filter(lambda x: x.id not in read, match_history))
    print("Total Aram Games:", len(match_history))
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

    dill.dump(matches, file = open("Aram_Data.pickle", "wb"))
    dill.dump(read, file = open("Read.pickle", "wb"))

    return matches



def win_rate(name, data):
    wins = 0
    losses = 0

    for i in data:
        if name in i.team_names[0]:
            if i.win:
                wins += 1
            else:
                losses += 1

    print(wins,losses,round(wins/(wins+losses)*100,2))
    print()



def champ_winrate(name, data):
    dic = defaultdict(lambda: (0, 0))

    for i in data:
        if name in i.team_names[0]:
            indx = i.team_names[0].index(name)
            champ = i.teamcomp[0][indx]
            if i.win:
                dic[champ] = (dic[champ][0] + 1, dic[champ][1])
            else:
                dic[champ] = (dic[champ][0], dic[champ][1] + 1)

    pretty(sorted(dic.items(), key=lambda item: item[1][0]+item[1][1], reverse=True), 15)
    print()



def champ_kda(name, data):
    dic = defaultdict(list)

    for i in data:
        if name in i.team_names[0]:
            indx = i.team_names[0].index(name)
            champ = i.teamcomp[0][indx]
            dic[champ].append(float(i.kda))

    dic = dict(map(lambda kv: (kv[0], round(sum(kv[1])/len(kv[1]), 2)), dic.items()))
    pretty(sorted(dic.items(), key=lambda item: item[1], reverse=True), 15)
    print()



def kda(data):
    kda = 0
    count = 0
    for i in data:
        kda += float(i.kda)
        count += 1
    print("KDA", round(kda/count,2))
    print()



def kp(data):
    kp = 0
    count = 0
    for i in data:

        if i.kp != 0:
            kp += float(i.kp)
            count += 1
    print("KP", round(kp/count,2))
    print()



def common_teammates(data, lookup=None):
    common = defaultdict(int)
    for i in data:
        for j in i.team_names[0]:
            common[j] += 1

    common = dict(filter(lambda x: x[1] >= 2, common.items()))
    pretty(sorted(common.items(), key=lambda item: item[1],reverse=True)[1:], 25)

    if lookup:
        print()
        print(lookup in common)
        if lookup in common:
            print(common[lookup])
    print()



def multikills(data):
    common = defaultdict(int)
    for i in data:
        if i.multikill:
            common[i.multikill] += 1
    pretty(sorted(common.items(), key=lambda item: item[1]), 10)
    print()


def items(data):
    common = defaultdict(int)
    for i in data:
        for j in i.items:
            common[j] += 1
    pretty(sorted(common.items(), key=lambda item: item[1],reverse=True)[1:], 30)
    print()

def adc_winrate(data):
    adcwin = 0
    adcloss = 0
    adcwin2 = 0
    adcloss2 = 0
    total_wins = 0
    total_losses = 0
    for x in data:
        if x.time:
            if x.win:
                total_wins += 1
                if set(x.teamcomp[0]).intersection(adcs) and not set(x.teamcomp[1]).intersection(adcs):
                    adcwin += 1
                if set(x.teamcomp[1]).intersection(adcs) and not set(x.teamcomp[0]).intersection(adcs):
                    adcwin2 += 1
            else:
                total_losses += 1
                if set(x.teamcomp[0]).intersection(adcs) and not set(x.teamcomp[1]).intersection(adcs):
                    adcloss += 1
                if set(x.teamcomp[1]).intersection(adcs) and not set(x.teamcomp[0]).intersection(adcs):
                    adcloss2 += 1

    win_rate =  (total_wins * 1.0 /(total_losses + total_wins))


    adcwin_rate = (adcwin * 1.0 / (adcwin + adcloss))
    noadcwin_rate = (adcwin2 * 1.0 / (adcwin2 + adcloss2))

    print("win_rate", win_rate *100)
    print("adcwin_rate", adcwin_rate*100)
    print("noadcwin_rate", noadcwin_rate*100)

    print("adc advantage", (adcwin_rate - win_rate)*100)

    print("no adc advantage", (noadcwin_rate - win_rate)*100)
    print()



def time_played(data):
    count = 0
    for i in data:
        count += i.time
    print(count/3600, "hours")
    print()



def win_rate_with(name, data):
    selfwin = 0
    with_other_win = 0
    selfloss = 0
    with_other_loss = 0
    for i in data:
        if i.time:
            if i.win:
                if name in i.team_names[0]:
                    with_other_win += 1
                else:
                    selfwin +=1
            else:
                if name in i.team_names[0]:
                    with_other_loss += 1
                else:
                    selfloss += 1

    if with_other_win + with_other_loss == 0:
        print("Wrong Name\n")
        return

    print("Winrate with " + str(name),100.0*with_other_win / (with_other_loss + with_other_win))
    print("Winrate without "+ str(name),100.0* selfwin / (selfwin + selfloss))
    print("Winrate Difference with "+ str(name), -1*((100.0* selfwin / (selfwin + selfloss))-(100.0*with_other_win / (with_other_loss + with_other_win))))
    print()


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
