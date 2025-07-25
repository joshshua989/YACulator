import pandas as pd
from bs4 import BeautifulSoup
import requests

url = "https://www.pro-football-reference.com/years/2024/games.htm"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
table = soup.find('table', {'id': 'games'})
df = pd.read_html(str(table))[0]

# Filter out rows like "Playoffs"
df = df[df['Week'].astype(str).str.isnumeric()]

# Fix column names just in case
df.columns = [col.strip() for col in df.columns]

# Rename for clarity
df.rename(columns={
    'Winner/tie': 'Winner',
    'Loser/tie': 'Loser',
    'PtsW': 'PtsW',
    'PtsL': 'PtsL',
    'YdsW': 'YdsW',
    'TOW': 'TOW',
    'YdsL': 'YdsL',
    'TOL': 'TOL'
}, inplace=True)

# Infer home/away: If '@' appears in any column, use it, otherwise fallback to row order
if '@' in df.columns:
    df['Home'] = df.apply(lambda row: row['Loser'] if row['@'] == '@' else row['Winner'], axis=1)
    df['Away'] = df.apply(lambda row: row['Winner'] if row['@'] == '@' else row['Loser'], axis=1)
else:
    # fallback: assume first team is home, second is away (not always correct)
    df['Home'] = df['Winner']
    df['Away'] = df['Loser']

# Final column selection
cols_to_keep = ['Week', 'Day', 'Date', 'Time', 'Winner', 'Loser', 'PtsW', 'PtsL', 'YdsW', 'TOW', 'YdsL', 'TOL', 'Home', 'Away']
df = df[[col for col in cols_to_keep if col in df.columns]]

# Save
df.to_csv("DATA/NFL_SCHEDULE_2024.csv", index=False)
print("✅ Saved: NFL_SCHEDULE_2024.csv")
