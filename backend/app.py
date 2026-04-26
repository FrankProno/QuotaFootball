from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QuotaFootball API attiva"}

@app.get("/teams")
def get_teams():
    df = pd.read_csv("data/teams.csv")
    return df.to_dict(orient="records")
