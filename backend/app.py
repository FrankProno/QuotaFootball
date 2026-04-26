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

@app.get("/predict")
def predict(team1: str, team2: str):
    return {
        "match": f"{team1} vs {team2}",
        "prediction": f"{team1} wins",
        "confidence": 0.65
    }
