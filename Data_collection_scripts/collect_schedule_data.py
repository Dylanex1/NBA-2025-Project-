import pandas as pd

months = ["october", "november", "december", "january", "february", "march", "april"]
base_url = "https://www.basketball-reference.com/leagues/NBA_2025_games-{}.html"

dfs = []
for month in months:
    url = base_url.format(month)
    tables = pd.read_html(url)  
    # print(tables)  # Checking the correct table is being collected
    df = tables[0]   # Extracting only table       
    dfs.append(df)   # Adding table to list of tables

# Stack rows
all_games = pd.concat(dfs, axis=0, ignore_index=True)

# Save file
all_games.to_csv("NBA_24_25_Schedule.csv", index=False)
