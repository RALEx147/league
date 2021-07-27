import pandas as pd
import plotly.express as px

def role_distribution(dataframe, champs):
    dataframe["role"] = dataframe.champ.apply(lambda x: champs[x])
    wr = round(dataframe[dataframe.win == True].groupby("role").win.count() / \
               dataframe.groupby("role").win.count() * 100, 2)

    chart = px.pie(dataframe.groupby("role").count().reset_index(), values="win", names="role")
    return wr, chart

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
    items = dataframe.summoner.apply(lambda x: [i.id for i in x.stats.items if i])
    return pd.Series([i for sublist in items for i in sublist]).value_counts().rename(item_id_to_name).drop(
        "Poro-Snax").head(show)






def wr(dataframe):
    wr = dataframe.win.value_counts(normalize=True).sort_index(ascending=False).rename(
        {True: "Win", False: "Loss"}).mul(100).round(1).astype(str) + '%'
    if "Win" in wr:
        wr["Win"] = wr["Win"] + " " + str(dataframe.win.value_counts().sort_index(ascending=False)[True])
    else:
        temp = wr["Loss"]
        del wr["Loss"]
        wr["Win"] = "0.0% 0"
        wr["Loss"] = temp

    if "Loss" in wr:
        wr["Loss"] = wr["Loss"] + " " + str(dataframe.win.value_counts().sort_index(ascending=False)[False])
    else:
        wr["Loss"] = "0.0% 0"

    return wr


def wl(dataframe, filter=3):
    wl = pd.DataFrame()

    wl["wins"] = dataframe[dataframe.win == True].summoner.apply(lambda x: x.champion).value_counts()
    wl["losses"] = dataframe[dataframe.win == False].summoner.apply(lambda x: x.champion).value_counts()
    wl["losses"].fillna(value=0, inplace=True)
    wl["total"] = wl.losses + wl.wins
    wl["wr"] = round(wl.wins / wl.total, 2) * 100

    return wl[wl.total >= filter].sort_values(by=["wr", "total"], ascending=False)

