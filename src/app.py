from fastapi import FastAPI, HTTPException
from pathlib import Path
import json
import os

app = FastAPI(title="NFL Team Stats API")

DATA_PATH = Path(__file__).resolve().parent.parent / "assets" / "teams.json"
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")


def load_teams():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/health")
def health_check():
    return {"status": "ok", "log_level": LOG_LEVEL}


@app.get("/teams")
def get_teams():
    return load_teams()


@app.get("/team/{team_name}")
def get_team(team_name: str):
    teams = load_teams()
    for team in teams:
        if team["name"].lower() == team_name.lower():
            return team
    raise HTTPException(status_code=404, detail="Team not found")


@app.get("/compare/{team_a}/{team_b}")
def compare_teams(team_a: str, team_b: str):
    teams = load_teams()

    def find(name: str):
        for t in teams:
            if t["name"].lower() == name.lower():
                return t
        return None

    a = find(team_a)
    b = find(team_b)

    if a is None or b is None:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    if a["name"].lower() == b["name"].lower():
        higher = "same team"
    elif a["points_scored"] > b["points_scored"]:
        higher = a["name"]
    elif a["points_scored"] < b["points_scored"]:
        higher = b["name"]
    else:
        higher = "tie"

    return {
        "team_a": a,
        "team_b": b,
        "higher_scoring_team": higher
    }
