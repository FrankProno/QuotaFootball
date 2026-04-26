from fastapi import FastAPI
import csv

app = FastAPI()

# funzione per leggere squadre
def load_teams():
    teams = []
    with open("backend/data/teams.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            teams.append({
                "id": int(row["id"]),
                "name": row["name"],
                "attack_rating": float(row["attack_rating"]),
                "defense_rating": float(row["defense_rating"])
            })
    return teams

@app.get("/")
def home():
    return {"message": "QuotaFootball API attiva"}

@app.get("/teams")
def get_teams():
    return load_teams()

@app.get("/predict")
def predict(team1: str, team2: str):
    teams = load_teams()

    t1 = next((t for t in teams if t["name"].lower() == team1.lower()), None)
    t2 = next((t for t in teams if t["name"].lower() == team2.lower()), None)

    if not t1 or not t2:
        return {"error": "Squadra non trovata"}

    # calcolo punteggio
    score1 = t1["attack_rating"] - t2["defense_rating"]
    score2 = t2["attack_rating"] - t1["defense_rating"]

    # probabilità (normalizzate)
    total = abs(score1) + abs(score2) + 0.0001
    prob1 = abs(score1) / total
    prob2 = abs(score2) / total

    if score1 > score2:
        prediction = f"{t1['name']} vince"
        confidence = round(prob1, 2)
    elif score2 > score1:
        prediction = f"{t2['name']} vince"
        confidence = round(prob2, 2)
    else:
        prediction = "Pareggio"
        confidence = 0.5

    return {
        "match": f"{team1} vs {team2}",
        "prediction": prediction,
        "confidence": confidence
    }
