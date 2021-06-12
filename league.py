from league_data import *
from league_functions import *
from league_constants import *
import Game
import sys
data = load_fetch_data(robb)

# Aram_Data = fetch_new_data(read_set, Aram_Data, robb)
d = defaultdict(int)
for i in data:
    d[type(i.summoner.stats).__name__] += 1

print(d)

for i in data:
    if type(i.summoner.stats).__name__ == "ParticipantStats":
        i.summoner.stats = Game.Stats(i.summoner.stats)

d = defaultdict(int)
for i in data:
    d[type(i.summoner.stats).__name__] += 1

print(d)

"""dill.dump(data, file = open("cache/data_dirty_doughnut.pickle", "wb"))
"""
# print(read_set)
# win_rate(robb, Aram_Data)
# champ_winrate(robb, Aram_Data)
# champ_kda(robb, Aram_Data)
# kda(Aram_Data)
# kp(Aram_Data)
# common_teammates(Aram_Data)
# multikills(Aram_Data)
# items(Aram_Data)
# adc_winrate(Aram_Data)
# time_played(Aram_Data)
# win_rate_with(thomas, Aram_Data)
# time_distribution(robb, Aram_Data)


# a  = dill.load(open("Aram_Data_New.pickle", "rb"))
# print(a[0].summoner.stats.first_inhibitor_kill)
