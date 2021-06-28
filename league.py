from league_data import *
from league_functions import *
from league_constants import *
import pandas as pd

# TODO -convert to pandas(fetch and append and storing too)
#      -finish fuctions -new function ideas
#      -filtering

data = load_fetch_data(robb)

# print(read_set)
# win_rate(data)
# champ_winrate(data)
# champ_kda(robb, Aram_Data)
# kda(Aram_Data)
# kp(Aram_Data)
# common_teammates(Aram_Data)
# multikills(Aram_Data)
# items(Aram_Data)
adc_winrate(data)
# time_played(Aram_Data)
# win_rate_with(thomas, Aram_Data)
# time_distribution(robb, data)


# a  = dill.load(open("Aram_Data_New.pickle", "rb"))
# print(a[0].summoner.stats.first_inhibitor_kill)
