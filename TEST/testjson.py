#!coding = utf-8
import json
from pprint import pprint


with open("./schedule_2016_03.json", encoding='utf8') as f:
    data = json.load(f)


want_data = data["payload"]["dates"][0]["games"][0]

def get_team_data(team_type):

    matchup = team_type["matchup"]
    confRank = matchup["confRank"]
    divRank = matchup["divRank"]
    losses = matchup["losses"]

    profile = team_type["profile"]
    abbr = profile["abbr"]
    city = profile["city"]
    cityEn = profile["cityEn"]
    code = profile["code"]
    conference = profile["conference"]




