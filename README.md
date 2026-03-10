# RAWG Video Games Dataset

## Overview
This repository contains a curated dataset of video games released between 2015 and 2025, collected from the [RAWG API](https://rawg.io/apidocs). The dataset includes over 500 games with features such as genre, rating, platforms, player type, and ESRB rating.  

The purpose of this dataset is to demonstrate data acquisition, cleaning, and preparation in Python.

## Dataset Features
| Column | Description |
|--------|-------------|
| `name` | Title of the game |
| `primary_genre` | Main genre of the game |
| `rating` | Average user rating (0–5) |
| `ratings_count` | Number of user ratings submitted |
| `release_year` | Year the game was released |
| `metacritic` | Metacritic score (0–100), if available |
| `playtime` | Typical hours to complete the game |
| `genre_count` | Number of genres assigned |
| `game_type` | Singleplayer, Multiplayer, Both, or None |
| `platform_count` | Total number of platforms |
| `pc` | Boolean: available on PC |
| `console` | Boolean: available on major consoles (PlayStation, Xbox, Switch) |
| `mobile` | Boolean: available on mobile devices (iOS/Android) |
| `esrb_rating` | ESRB rating (e.g., Mature, Teen, Everyone) |

## Data Acquisition
The data was collected using Python (`requests` and `pandas`) to access the RAWG API. Requests were paginated and a small delay was added to avoid overloading the API. Users must provide their own API key via an `.env` file — no private keys are included in this repo.  

## Usage
1. Clone the repository.  
2. Install dependencies:  
```bash
pip install -r requirements.txt
```

Add your RAWG API key in a .env file:

```py
RAWG_API_KEY=your_api_key_here
```

Run the rawg_data_collection.ipynb notebook to reproduce the dataset.

The final dataset is also included as game_dataset.csv for convenience.
