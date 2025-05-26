import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

appids = [730, 570, 578080, 1172470, 3164500, 2694490, 2923300, 431960, 3419430, 2246340, 252490, 2767030, 1203220, 2507950, 271590, 1086940, 413150, 236390, 480, 3241660, 2252570, 
          3240220, 1938090, 230410, 1366800, 359550, 1174180, 286690, 2669320, 381210, 394360, 440, 322330, 1245620, 221100, 1281930, 3188910, 438100, 289070, 105600, 227300, 
          1782210, 1222670, 2878980, 3117820, 294100, 1623730, 346110, 1973530, 1364780]

now = datetime.now(timezone.utc)
thirty_days_ago = now - timedelta(days=30)
thirty_days_ago_ts = int(thirty_days_ago.timestamp() * 1000)

def get_game_metadata(appid):
    try:
        res = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
        res.raise_for_status()
        data = res.json()
        game_data = data[str(appid)]
        if game_data["success"]:
            name = game_data["data"].get("name", f"Unknown_{appid}")
            genres = game_data["data"].get("genres", [])
            genre_names = ", ".join([g["description"] for g in genres]) if genres else "Unknown"
            return name, genre_names
    except Exception as e:
        print(f"Failed to get metadata for {appid}: {e}")
    return f"Unknown_{appid}", "Unknown"

all_data = []

for appid in appids:
    name, genres = get_game_metadata(appid)
    try:
        url = f"https://steamcharts.com/app/{appid}/chart-data.json"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        for timestamp, avg_players in data:
            if timestamp >= thirty_days_ago_ts:
                date = pd.to_datetime(timestamp, unit="ms")
                all_data.append({
                    "Game": name,
                    "Genre": genres,
                    "Date": date,
                    "AvgPlayers": avg_players
                })
    except Exception as e:
        print(f"Failed to fetch chart data for {name} (AppID {appid}): {e}")

df = pd.DataFrame(all_data)
df.sort_values(by=["Game", "Date"], inplace=True)
df.to_csv("steamcharts_30_days_2.csv", index=False)