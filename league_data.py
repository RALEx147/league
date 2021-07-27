import os
import time
import dill
from Game import Match, Summoner, Stats, Player

import cassiopeia as cass
import pandas as pd
import credential


def _convert_df(data):
    return pd.DataFrame([vars(d) for d in data])


def load_fetch_data(name):
    try:
        aram_data, read_set = _load_data(name)
    except:
        aram_data, read_set = pd.DataFrame(data=None, columns = ['duration', 'patch', 'id', 'creation', 'surrender', 'blue', 'red', 'summoner', 'side']), set()

    return _fetch_new_data(read_set, aram_data, name)


def _load_data(name):
    aram_data = pd.read_pickle("cache/data_" + name.lower().replace(" ", "_") + ".pickle")
    read_set = dill.load(open("cache/read_" + name.lower().replace(" ", "_") + ".pickle", "rb"))
    print("DATA LOADED", len(aram_data))
    return aram_data, read_set


def _fetch_new_data(read, matches, name):
    last_updated = 0
    try:
        last_updated = os.stat("cache/data_" + name.lower().replace(" ", "_") + ".pickle").st_mtime
    except:
        pass
    if time.time() - last_updated > 10000:
        cass.apply_settings({"logging": {"print_calls": False}})
        cass.set_riot_api_key(credential.get_key())

        summoner = cass.get_summoner(name=name, region="NA")

        champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region="NA")}
        summonerspell_id_to_name_mapping = {spell.id: spell.name for spell in cass.get_summoner_spells(region="NA")}

        print("Getting Match History")
        match_history = cass.get_match_history(summoner=summoner, queues=[cass.Queue.aram])
        print("Total Games:", len(match_history))
        match_history = list(filter(lambda x: x.id not in read, match_history))
        print("NEW Games:", len(match_history))
        print("Getting Game Data")

        count = 0
        new_matches = []
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

            surrender = ((match.blue_team.win and match.blue_team.tower_kills != 4) or (match.red_team.win and match.red_team.tower_kills != 4))
            game = Match(match.duration, match.patch, match.id, match.creation, surrender, blue, red, main_summoner, side)
            new_matches.append(game)
            read.add(match.id)
            count += 1

        print("DATA ADDED", count, '\n')
        matches = pd.concat([matches, _convert_df(new_matches)])
        pd.to_pickle(matches, filepath_or_buffer=str("cache/data_" + name.lower().replace(" ", "_") + ".pickle"))
        dill.dump(read, file=open("cache/read_" + name.lower().replace(" ", "_") + ".pickle", "wb"))
    else:
        print("NO DATA ADDED\n")
    return matches

# cass.set_riot_api_key(credential.get_key())
# s = cass.get_summoner(name="Dirty Doughnut", region="NA")
# match_history = cass.get_match_history(summoner=s, queues=[cass.Queue.aram])
