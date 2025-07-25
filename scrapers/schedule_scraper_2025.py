import pandas as pd
from bs4 import BeautifulSoup
import requests

url = "https://www.pro-football-reference.com/years/2025/games.htm"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
table = soup.find('table', {'id': 'games'})

# Read and keep regular season games
df = pd.read_html(str(table))[0]
df = df[df['Week'].astype(str).str.isnumeric()]

# Select and rename only the correct columns
df = df[[
    'Week',
    'Day',
    'Unnamed: 2',
    'VisTm',       # Visitor
    'Pts',         # VisitorPts
    'HomeTm',      # Home
    'Pts.1',       # HomePts
    'Time'
]].rename(columns={
    'Unnamed: 2': 'Date',
    'VisTm': 'Visitor',
    'Pts': 'VisitorPts',
    'HomeTm': 'Home',
    'Pts.1': 'HomePts'
})

# Strip string columns
for col in ['Week', 'Day', 'Date', 'Visitor', 'Home', 'Time']:
    df[col] = df[col].astype(str).str.strip()

# Clean numeric scores
df['VisitorPts'] = pd.to_numeric(df['VisitorPts'], errors='coerce')
df['HomePts'] = pd.to_numeric(df['HomePts'], errors='coerce')

# Save clean full schedule
df.to_csv("DATA/NFL_SCHEDULE_2025.csv", index=False)
print("✅ NFL_SCHEDULE_2025.csv saved with clean column names and full data.")
