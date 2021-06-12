from league_functions import *
from league_constants import *



try:
    Aram_Data, read_set = load_data_old("Aram_Data_OLD2.pickle", "read_set.pickle")
except:
    Aram_Data, read_set = [], set()

Aram_Data = fetch_new_data_old(read_set, Aram_Data)

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
