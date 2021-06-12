import os
import time
from collections import namedtuple
import dill
from Game import Match, Summoner, Stats
import cassiopeia as cass

def load_fetch_data(name):
    try:
        Aram_Data, read_set = _load_data(name)
    except:
        Aram_Data, read_set = [], set()

    return _fetch_new_data(read_set, Aram_Data, name)

def _load_data(name):
    Aram_Data = dill.load(open("cache/data_"+ name.lower().replace(" ", "_")+".pickle", "rb"))
    read_set = dill.load(open("cache/read_"+ name.lower().replace(" ", "_")+".pickle", "rb"))
    print("DATA LOADED",len(Aram_Data))
    return Aram_Data, read_set


def _fetch_new_data(read, matches, name):
    last_updated = 0
    try:
        last_updated = os.stat("cache/data_"+ name.lower().replace(" ", "_")+".pickle").st_mtime
    except:
        pass
    if time.time() - last_updated > 3600:
        cass.apply_settings({"logging": {"print_calls": False}})
        cass.set_riot_api_key("***REMOVED***")

        summoner = cass.get_summoner(name=name, region="NA")

        Player = namedtuple('Player', ['name', 'champ'])
        champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region="NA")}
        summonerspell_id_to_name_mapping = {spell.id: spell.name for spell in cass.get_summoner_spells(region="NA")}

        print("Getting Match History")
        match_history = cass.get_match_history(summoner=summoner, queues=[cass.Queue.aram])
        print("Total Games:", len(match_history))
        match_history = list(filter(lambda x: x.id not in read, match_history))
        print("NEW Games:", len(match_history))
        print("Getting Game Data")

        count = 0
        for match in match_history:
            if count % 100 == 0 and count > 0:
                print(round(count * 100 / len(match_history)), '/ 100')
            blue = []
            red = []
            main_summoner = None
            side = None

            for i in match.participants:
                if i.side.value == 100:
                    blue.append(Player(i.summoner.name, champion_id_to_name_mapping[i.champion.id]))
                else:
                    red.append(Player(i.summoner.name, champion_id_to_name_mapping[i.champion.id]))

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
                    main_summoner = Summoner(summoner_spell_d, summoner_spell_f, runes, stats, champion)

            game = Match(match.duration, match.season, match.patch, match.id, blue, red, main_summoner, side)
            matches.append(game)
            read.add(match.id)
            count += 1

        print("DATA ADDED", count, '\n')

        dill.dump(matches, file = open("cache/data_"+ name.lower().replace(" ", "_")+".pickle", "wb"))
        dill.dump(read, file = open("cache/read_"+ name.lower().replace(" ", "_")+".pickle", "wb"))
    else:
        print("NO DATA ADDED\n")
    return matches
