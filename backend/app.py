from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ODDS_API_KEY = os.getenv("ODDS_API_KEY", "INSERISCI_ODDS_KEY")
FOOTBALL_DATA_KEY = os.getenv("FOOTBALL_DATA_KEY", "INSERISCI_FOOTBALL_DATA_KEY")

@app.get("/")
def home():
    return {"message": "QuotaFootball API attiva"}

@app.get("/teams")
def get_teams(season: int = 2025):
    url = f"https://api.football-data.org/v4/competitions/SA/teams?season={season}"
    headers = {"X-Auth-Token": FOOTBALL_DATA_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        teams = []
        for item in data.get("teams", []):
            teams.append({
                "name": item.get("name"),
                "shortName": item.get("shortName"),
                "crest": item.get("crest")
            })

        return {"season": season, "teams": teams}

    except Exception as e:
        return {"error": str(e), "teams": []}

@app.get("/odds")
def get_odds(team1: str, team2: str):
    url = "https://api.the-odds-api.com/v4/sports/soccer_italy_serie_a/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if isinstance(data, dict) and "message" in data:
            return {"error": data["message"], "results": []}

        results = []

        for match in data:
            home = match.get("home_team", "")
            away = match.get("away_team", "")

            if team1.lower() in home.lower() and team2.lower() in away.lower() or team2.lower() in home.lower() and team1.lower() in away.lower():
                for bookmaker in match.get("bookmakers", []):
                    markets = bookmaker.get("markets", [])
                    if not markets:
                        continue

                    results.append({
                        "bookmaker": bookmaker.get("title"),
                        "odds": markets[0].get("outcomes", [])
                    })

        return {"results": results}

    except Exception as e:
        return {"error": str(e), "results": []}
