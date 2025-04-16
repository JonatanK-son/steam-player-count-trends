import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone

# Fetch data from SteamCharts
url = "https://steamcharts.com/app/730/chart-data.json"
res = requests.get(url)
data = res.json()

# Get current time and time 30 days ago
now = datetime.now(timezone.utc)
thirty_days_ago = now - timedelta(days=30)

thirty_days_ago_ts = int(thirty_days_ago.timestamp() * 1000)

# Filter and print only the last 30 days
for timestamp, avg_players in data:
    if timestamp >= thirty_days_ago_ts:
        date = pd.to_datetime(timestamp, unit="ms")
        print(f"{date}: {avg_players} players")