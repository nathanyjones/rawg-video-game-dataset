import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time
from datetime import datetime

# Load API key
load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
base_url = "https://api.rawg.io/api"

# Fetch data
game_data = []
for i in range(1, 51):
    url = f"{base_url}/games?key={API_KEY}&dates=2015-01-01,2025-12-31&page={i}"
    response = requests.get(url)
    game_data.extend(response.json()['results'])
    time.sleep(0.2)

# Convert to DataFrame
game_df = pd.DataFrame(game_data)
game_df = game_df[['name', 'released', 'rating', 'ratings_count', 'metacritic', 'playtime', 'platforms', 'genres', 'tags', 'esrb_rating']]
game_df['release_year'] = pd.to_datetime(game_df['released']).dt.year
game_df = game_df.drop(columns=['released'])

# Categorize platforms
def categorize_platforms(platforms):
    pc = any(p['platform']['name'] == 'PC' for p in platforms)
    console = any(p['platform']['name'] in ['PlayStation 4', 'PlayStation 5', 'Xbox One', 'Xbox Series S/X', 'Nintendo Switch'] for p in platforms)
    mobile = any(p['platform']['name'] in ['iOS', 'Android'] for p in platforms)
    return pd.Series({'pc': pc, 'console': console, 'mobile': mobile})

game_df[['pc', 'console', 'mobile']] = game_df['platforms'].apply(categorize_platforms)
game_df['platform_count'] = game_df['platforms'].apply(lambda x: len(x))
game_df = game_df.drop(columns=['platforms'])

# Determine player type
def game_player_type(tags):
    has_single = any(tag['name'] == 'Singleplayer' for tag in tags)
    has_multi = any(tag['name'] == 'Multiplayer' for tag in tags)
    
    if has_single and has_multi:
        return 'Both'
    elif has_single:
        return 'Singleplayer'
    elif has_multi:
        return 'Multiplayer'
    else:
        return 'None'

game_df['game_type'] = game_df['tags'].apply(game_player_type)
game_df = game_df.drop(columns=['tags'])

# Handle genres
game_df['genres'] = game_df['genres'].apply(lambda x: [g['name'] for g in x])
game_df['primary_genre'] = game_df['genres'].apply(lambda x: x[0] if x else None)
game_df['genre_count'] = game_df['genres'].apply(lambda x: len(x))
game_df = game_df.drop(columns='genres')

# Clean ESRB
game_df['esrb_rating'] = game_df['esrb_rating'].apply(lambda x: x['name'] if x else None)

# Reorder and sort
game_df = game_df[['name', 'primary_genre', 'rating', 'ratings_count', 'release_year',
                   'metacritic', 'playtime', 'genre_count', 'game_type',
                   'platform_count', 'pc', 'console', 'mobile', 'esrb_rating']]
game_df = game_df.sort_values(by='rating', ascending=False).reset_index(drop=True)

# Save to CSV
game_df.to_csv('game_dataset.csv', index=False)
print("Dataset saved as 'game_dataset.csv'.")