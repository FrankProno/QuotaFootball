from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# ✅ CORS (fondamentale per GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Variabili ambiente
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "INSERISCI_ODDS_KEY")
FOOTBALL_DATA_KEY = os.getenv("FOOTBALL_DATA_KEY", "INSERISCI_FOOTBALL_DATA_KEY")

@app.get("/")
def home():
    return {"message": "QuotaFootball API attiva"}

# ✅ TEAMS (automatico + fallback)
@app.get("/teams")
def get_teams(season: int = 2025):

    fallback = [
        {"name": "Inter"}, {"name": "Juventus"}, {"name": "Milan"},
        {"name": "Napoli"}, {"name": "Roma"}, {"name": "Lazio"},
        {"name": "Atalanta"}, {"name": "Fiorentina"}, {"name": "Bologna"},
        {"name": "Torino"}, {"name": "Genoa"}, {"name": "Udinese"},
        {"name": "Lecce"}, {"name": "Cagliari"}, {"name": "Verona"},
        {"name": "Como"}, {"name": "Parma"}, {"name": "Pisa"},
        {"name": "Sassuolo"}, {"name": "Cremonese"}
    ]

    try:
        url = f"https://api.football-data.org/v4/competitions/SA/teams?season={season}"
        headers = {"X-Auth-Token": FOOTBALL_DATA_KEY}

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        teams = []
        for item in data.get("teams", []):
            teams.append({
                "name": item.get("name"),
                "shortName": item.get("shortName")
            })

        # 🔁 fallback se API non risponde
        if len(teams) == 0:
            return {"teams": fallback}

        return {"teams": teams}

    except Exception:
        return {"teams": fallback}

# ✅ ODDS REALI
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

        # ❌ errore API
        if isinstance(data, dict) and "message" in data:
            return {"error": data["message"], "results": []}

        results = []

        for match in data:
            home = match.get("home_team", "")
            away = match.get("away_team", "")

            # 🔎 trova match giusto
            if (team1.lower() in home.lower() and team2.lower() in away.lower()) or \
               (team2.lower() in home.lower() and team1.lower() in away.lower()):

                for bookmaker in match.get("bookmakers", []):
                    markets = bookmaker.get("markets", [])
                    if not markets:
                        continue

                    results.append({
                        "bookmaker": bookmaker.get("title"),
                        "odds": markets[0].get("outcomes", [])
                    })

        # ❌ nessuna quota trovata
        if len(results) == 0:
            return {"error": "Nessuna quota trovata", "results": []}

        return {"results": results}

    except Exception as e:
        return {"error": str(e), "results": []}
