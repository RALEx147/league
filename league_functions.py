from collections import defaultdict
import numpy as np

def pretty(d, length):
    for key, value in d:
        space = " " * (length - len(key))
        print(str(key)+space+str(value))




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
    print("Win Standerd Deviation", (np.std(win_times))/60)
    print("Loss Standerd Deviation", (np.std(loss_times))/60)
    print("Standerd Deviation",(np.std(win_times + loss_times))/60)
    print()
