from fastapi import FastAPI
import csv

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QuotaFootball API attiva"}

@app.get("/teams")
def get_teams():
    teams = []
    with open("backend/data/teams.csv", newline='', encoding='utf-8') as csvfile:
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
        "prediction": "Team1 win",
        "confidence": 0.65
    }
