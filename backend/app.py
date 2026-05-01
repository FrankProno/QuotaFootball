from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# ✅ CORS FIX (fondamentale per GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "QuotaFootball API"}

@app.get("/teams")
def get_teams():
    teams = []
    with open("data/teams.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            teams.append({
                "id": int(row["id"]),
                "name": row["name"],
                "attack_rating": float(row["attack_rating"]),
                "defense_rating": float(row["defense_rating"])
            })
    return teams

@app.import math

import math
import random

@app.get("/predict")
def predict(team1: str, team2: str):
    teams = get_teams()

    t1 = next(t for t in teams if t["name"] == team1)
    t2 = next(t for t in teams if t["name"] == team2)

    # forza squadre
    strength1 = t1["attack_rating"] - t2["defense_rating"]
    strength2 = t2["attack_rating"] - t1["defense_rating"]

    prob1 = 1 / (1 + math.exp(-strength1))
    prob2 = 1 / (1 + math.exp(-strength2))
    draw_prob = 1 - abs(prob1 - prob2)

    total = prob1 + prob2 + draw_prob
    prob1 /= total
    prob2 /= total
    draw_prob /= total

    odds1 = round(1 / prob1, 2)
    oddsX = round(1 / draw_prob, 2)
    odds2 = round(1 / prob2, 2)

    # OVER/UNDER (semplice modello)
    expected_goals = (t1["attack_rating"] + t2["attack_rating"]) / 2

    over25_prob = min(0.9, expected_goals / 3)
    under25_prob = 1 - over25_prob

    odds_over = round(1 / over25_prob, 2)
    odds_under = round(1 / under25_prob, 2)

    # MARCATORI (mock intelligente)
    players = {
        team1: ["Attaccante 1", "Attaccante 2"],
        team2: ["Attaccante A", "Attaccante B"]
    }

    scorer = random.choice(players[team1] + players[team2])

    return {
        "match": f"{team1} vs {team2}",
        "odds": {
            "1": odds1,
            "X": oddsX,
            "2": odds2
        },
        "over_under": {
            "over_2_5": odds_over,
            "under_2_5": odds_under
        },
        "top_scorer_prediction": scorer
    }
    }
