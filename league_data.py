import json
import os
from collections import defaultdict
from datetime import datetime
import tqdm

import dill
import pandas as pd
from riotwatcher import LolWatcher

import credential
from league_constants import dropped

lol_watcher = LolWatcher(credential.get_key())


def load_fetch_data(player):
    try:
        aram_data, read_set, name_set = _load_data(player)
    except FileNotFoundError:
        print("NEW USER, CREATING EMPTY CACHE")
        aram_data, read_set, name_set = pd.DataFrame(), set(), defaultdict(set)
    finally:
        return _fetch_new_data(aram_data, read_set, name_set, player)


def _load_data(name):
    aram_data = pd.read_pickle("cache/" + name.lower().replace(" ", "_") + "_data.pickle")
    read_set = dill.load(open("cache/" + name.lower().replace(" ", "_") + "_read.pickle", "rb"))
    name_set = dill.load(open("cache/" + name.lower().replace(" ", "_") + "_names.pickle", "rb"))
    print("DATA LOADED", len(aram_data))
    return aram_data, read_set, name_set


def _fetch_new_data(matches, read, names, player):
    last_updated = 0
    try:
        last_updated = os.stat("cache/" + player.lower().replace(" ", "_") + "_data.pickle").st_mtime
    except FileNotFoundError:
        pass

    summoner = lol_watcher.summoner.by_name('na1', player)
    match_ids = get_match_ids(summoner)
    match_ids -= read

    print(len(match_ids), "NEW MATCHES SINCE", datetime.fromtimestamp(last_updated))

    if match_ids:
        new_matches, summoner_names = get_matches(match_ids, summoner)
        matches = matches.append(new_matches)
        ids = set(matches.gameId.apply(lambda x: "NA1_" + str(x)))
        for k, v in summoner_names.items():
            names[k].update(v)

        pd.to_pickle(matches, filepath_or_buffer=str("cache/" + player.lower().replace(" ", "_") + "_data.pickle"))
        dill.dump(ids, file=open("cache/" + player.lower().replace(" ", "_") + "_read.pickle", "wb"))
        dill.dump(names, file=open("cache/" + player.lower().replace(" ", "_") + "_names.pickle", "wb"))
    else:
        print("NO DATA ADDED\n")

    return matches, names


def get_match_ids(summoner):
    index = 0
    match_ids = set()
    prev = -1
    while len(match_ids) != prev:
        prev = len(match_ids)
        match_ids.update(lol_watcher.match.matchlist_by_puuid(
            region="Americas",
            puuid=summoner['puuid'],
            count=100,
            start=(index * 100),
            queue=450))
        index += 1

    return match_ids


def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], a)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, str(i))
                i += 1
        else:
            out[name] = x

    flatten(y)
    return out


def get_matches(ids, summoner):
    summoners = defaultdict(set)

    matches = []
    for match in tqdm.tqdm(ids):
        match_data = lol_watcher.match.by_id("Americas", match)
        participants = match_data["metadata"]["participants"]
        match = match_data["info"]
        player_index = participants.index(summoner['puuid'])
        player_info = match["participants"][player_index]
        side = player_info["teamId"]

        team = []
        champs = []
        other_team = []
        other_champs = []
        for j in match["participants"]:
            if j["teamId"] == side:
                team.append(j["puuid"])
                champs.append(j["championId"])
            else:
                other_team.append(j["puuid"])
                other_champs.append(j["championId"])

            summoners[j["puuid"]].add(j["summonerName"])

        match["participants"] = match["participants"][player_index]
        runes = player_info["perks"]
        del match["teams"]
        del match["participants"]["perks"]
        if "gameEndTimestamp" in match:
            del match["gameEndTimestamp"]
        flattened = flatten_data(match)
        flattened["perks"] = runes
        flattened["team"] = team
        flattened["champs"] = champs
        flattened["other_team"] = other_team
        flattened["other_champs"] = other_champs

        matches.append(flattened)

    df = pd.read_json(json.dumps(matches))
    df.drop(dropped, axis=1, inplace=True, errors='ignore')
    df.gameStartTimestamp = pd.to_datetime(df.gameStartTimestamp, unit='ms')
    df.gameStartTimestamp = df.gameStartTimestamp.dt.tz_localize('UTC').dt.tz_convert('US/Pacific')
    df.gameDuration = df.gameDuration.apply(lambda x: int(x / 1000) if x > 3600 else x)
    return df, summoners


"""
    Test
"""


def load_legacy_data(name):

    aram_data = pd.read_pickle("aram_data/raw_old/data_" + name.lower().replace(" ", "_") + ".pickle")
    print("LEGACY DATA LOADED", len(aram_data))
    return aram_data

