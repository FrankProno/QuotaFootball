from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
import requests

app = FastAPI()

# CORS per GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ CAMBIA QUESTA DOPO
API_KEY = "f84e543d890f114b97d7e972b08a4c3b"

@app.get("/")
def home():
    return {"message": "QuotaFootball API attiva"}

@app.get("/teams")
def get_teams():
    teams = []
    with open("data/teams.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            teams.append(row["name"])
    return teams

@app.get("/odds")
def get_odds(team1: str, team2: str):
    url = "https://api.the-odds-api.com/v4/sports/soccer_italy_serie_a/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "h2h"
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []

    for match in data:
        # match più preciso
        if team1.lower() in match["home_team"].lower() or team2.lower() in match["away_team"].lower():

            for book in match["bookmakers"]:
                outcomes = book["markets"][0]["outcomes"]

                results.append({
                    "bookmaker": book["title"],
                    "odds": outcomes
                })

    return results
