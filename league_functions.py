from collections import defaultdict
import numpy as np
from league_constants import adcs

def pretty(d, length, addendum=None):
    for _, (key, value) in enumerate(d):
        space = " " * (length - len(key))
        if addendum:
            print(key, space, value, addendum[key])
        else:
            print(key, space, value)


def percent(wins, losses):
    if (wins + losses) == 0:
        return -1
    return round(100*wins/(wins+losses), 2)


def win_rate(data):
    d = defaultdict(int)
    for i in data:
        d[i.summoner.stats.win] += 1
    wins = d[True]
    losses = d[False]
    print(f'Wins: {wins}\nLosses: {losses}\n{percent(wins, losses)}%')
    return wins, losses

def champ_winrate(data):
    d = defaultdict(lambda : [0,0])
    percentages = {}
    for i in data:
        d[i.summoner.champion][0] += 1 if i.summoner.stats.win else 0
        d[i.summoner.champion][1] += 0 if i.summoner.stats.win else 1
    for key in d.keys():
        percentages[key] = str(percent(d[key][0], d[key][1])) + "%"

    pretty(sorted(d.items(), key=lambda item: item[1][0]+item[1][1], reverse=True), 15, addendum=percentages)

# def champ_kda(name, data):
# def kda(data):
# def kp(data):
# def common_teammates(data, lookup=None):
# def multikills(data):
# def items(data):
def adc_winrate(data):
    with_adc_wins = 0
    with_adc_losses = 0
    no_adc_wins = 0
    no_adc_losses = 0
    for i in data:
        blue = {i.champ for i in i.blue}
        red = {i.champ for i in i.red}
        personal = red if i.side else blue
        other = blue if i.side else red

        win = i.winning_side()
        if adcs&personal and not adcs&other:
            if win == i.side:
                with_adc_wins += 1
            else:
                with_adc_losses += 1
        if not adcs&personal and adcs&other:
            if win == i.side:
                no_adc_wins += 1
            else:
                no_adc_losses += 1

    print(f'With adc winrate: {percent(with_adc_wins, with_adc_losses)}%\nNo adc winrate: {percent(no_adc_wins, no_adc_losses)}%\n')

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
    print("Win Standerd Deviation", (np.std(win_times))/60)
    print("Loss Standerd Deviation", (np.std(loss_times))/60)
    print("Standerd Deviation",(np.std(win_times + loss_times))/60)
    print()
