import pandas as pd
import plotly.express as px
import cassiopeia as cass


def percent(num, denom):
    return str(round(len(num) / len(denom) * 100, 2))


def get_id_mappings():
    ver = cass.get_version(region="NA")
    item_id_to_name = {item.id: item.name for item in cass.core.staticdata.Items(region="NA", version=ver)}
    champ_id_to_name = {champ.id: champ.name for champ in cass.core.staticdata.Champions(region="NA", version=ver)}
    champ_name_to_id = {champ.name: champ.id for champ in cass.core.staticdata.Champions(region="NA", version=ver)}
    return item_id_to_name, champ_id_to_name, champ_name_to_id


def get_champ_roles():
    champs = pd.Series(cass.get_champions(region="NA"))
    champs.index = champs.apply(lambda x: x.name)
    champs = champs.apply(lambda x: x.tags[0])
    champs["Teemo"] = "Mage"
    champs["Graves"] = "Fighter"
    champs["Kayle"] = "Marksman"
    champs["Dr. Mundo"] = "Tank"

    adc = set(champs[champs.apply(lambda x: "Marksman" in x)].index)
    assassin = set(champs[champs.apply(lambda x: "Assassin" in x)].index)
    fighter = set(champs[champs.apply(lambda x: "Fighter" in x)].index)
    support = set(champs[champs.apply(lambda x: "Support" in x)].index)
    tank = set(champs[champs.apply(lambda x: "Tank" in x)].index)
    mage = set(champs[champs.apply(lambda x: "Mage" in x)].index)

    return champs, adc, assassin, fighter, support, tank, mage


def role_distribution(dataframe, champs, map):
    dataframe["role"] = dataframe.championId.apply(lambda x: champs[map[x]])
    wr = round(dataframe[dataframe.win == True].groupby("role").win.count() /
               dataframe.groupby("role").win.count() * 100, 2).apply(lambda x: str(x) + "%")

    count = dataframe.groupby("role").count().reset_index()
    sum = dataframe.groupby("role").sum().reset_index()
    avg = dataframe.groupby("role").mean().reset_index()
    return wr, count, sum, avg

def game_in_timeframe(dataframe, timeframe="Day"):
    if timeframe == "Day":
        dataframe["date"] = dataframe.creation.apply(lambda x: x.date())
    elif timeframe == "Month":
        dataframe["date"] =  dataframe.creation.apply(lambda x: (x.month, x.year))
    else:
        return
    games_in_day = dataframe.groupby("date").duration.agg(['sum','count']).sort_values("sum", ascending=False).head(10)
    games_in_day["sum"] = games_in_day["sum"].apply(lambda x:str(int(x//3600)) + "h " + str(int(x%3600//60))+"m")
    return games_in_day.head(3)




def games_in_days(dataframe, days=1):
    from datetime import timedelta
    start = 0
    end = 1
    max_games = 0
    result = (0, 0)

    for i in range(1, len(dataframe)):
        first = dataframe.creation.iloc[start]
        next = dataframe.creation.iloc[i]

        if first - next < timedelta(days):
            end += 1
        else:
            while dataframe.creation.iloc[start] - next > timedelta(days):
                start += 1
            end += 1

        if end - start > max_games:
            max_games = end - start
            result = (start, end)

    start = dataframe.iloc[result[0]]
    end = dataframe.iloc[result[1] - 1]
    diff = start.creation - end.creation

    print(max_games - 1, f"games in range of {diff} on {dataframe.iloc[result[0]].creation.strftime('%m-%d-%Y')}")
    return result


def max_kills(dataframe, games=5):
    dataframe["kills"] = dataframe.summoner.apply(lambda x: x.stats.kills)
    return dataframe.sort_values(by="kills", ascending=False).drop(["teamnames", "teamcomp", "enemynames", "enemycomp"],
                                                                   axis=1).head(games)


def max_kills_permin(dataframe, games=5):
    dataframe["kills"] = dataframe.summoner.apply(lambda x: x.stats.kills)
    dataframe["kpm"] = dataframe.kills / dataframe.duration * 60
    return dataframe.sort_values(by="kpm", ascending=False).drop(["teamnames", "teamcomp", "enemynames", "enemycomp"],
                                                                 axis=1).head(games)


def sums_count(dataframe):
    d = dataframe.summoner.apply(lambda x: x.summoner_spell_d)
    f = dataframe.summoner.apply(lambda x: x.summoner_spell_f)
    return d.append(f).value_counts()


def item_count(dataframe, item_id_to_name, show=5):
    return pd.Series([i for sublist in dataframe["items"] for i in sublist]).value_counts().rename(item_id_to_name).drop(
        "Poro-Snax").head(show)






def wr(dataframe, just_win=True):
    count = dataframe.win.value_counts()
    wr = dataframe.win.value_counts(normalize=True).sort_index(ascending=False).rename(
        {True: "Win", False: "Loss"}).mul(100).round(1).astype(str) + '%'

    if "Win" not in wr:
        wr = wr.append(pd.Series(["0.0%"], index=["Win"]))
    if "Loss" not in wr:
        wr = wr.append(pd.Series(["0.0%"], index=["Loss"]))

    wr.sort_index(ascending=False, inplace=True)
    wr["Win"] = wr["Win"] + " " + str(count[True] if True in count else 0)
    wr["Loss"] = wr["Loss"] + " " + str(count[False] if False in count else 0)
    if just_win:
        return wr["Win"]
    return wr


def wl(dataframe, filter=3):

    w = dataframe[dataframe.win == True].championId.value_counts()
    l = dataframe[dataframe.win == False].championId.value_counts()
    wl = pd.concat([w, l], axis=1)
    wl.columns = ['wins', 'losses']
    wl.fillna(value=0, inplace=True)
    wl["total"] = wl.wins + wl.losses
    wl = wl.astype(int)
    wl = wl.drop('losses', axis=1)
    wl["wr"] = round(wl.wins / wl.total, 2) * 100

    return wl[wl.total >= filter].sort_values(by=["wr", "total"], ascending=False)

