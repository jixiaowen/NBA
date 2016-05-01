#!/usr/bin/env python3
# coding = utf-8
import json


def get_team_data(team_type):
    matchup = team_type["matchup"]
    confrank = matchup["confRank"]
    divrank = matchup["divRank"]
    losses = matchup["losses"]
    profile = team_type["profile"]
    abbr = profile["abbr"]
    city = profile["city"]
    cityen = profile["cityEn"]
    code = profile["code"]
    conference = profile["conference"]
    displayabbr = profile["displayAbbr"]
    displayconference = profile["displayConference"]
    division = profile["division"]
    team_id = profile["id"]
    isallstarteam = profile["isAllStarTeam"]
    isleagueteam = profile["isLeagueTeam"]
    name = profile["name"]
    nameen = profile["nameEn"]

    return (confrank, divrank, losses, abbr, city, cityen, code, conference, displayabbr,
            displayconference, division, team_id, isallstarteam, isleagueteam, name, nameen)


def get_match_data(in_data):
    boxscore = in_data["boxscore"]
    attendance = boxscore["attendance"]
    awayscore = boxscore["awayScore"]
    gamelength = boxscore["gameLength"]
    homescore = boxscore["homeScore"]
    match_profile = in_data["profile"]
    arenalocation = match_profile["arenaLocation"]
    arenaname = match_profile["arenaName"]
    awayteamid = match_profile["awayTeamId"]
    gameid = match_profile["gameId"]
    hometeamid = match_profile["homeTeamId"]
    seasontype = match_profile["seasonType"]
    utcmillis = match_profile["utcMillis"]
    away_team_data = get_team_data(want_data["awayTeam"])
    home_team_data = get_team_data(want_data["homeTeam"])
    match_data = (gameid, hometeamid, awayteamid, seasontype, arenalocation, arenaname,
                  attendance, homescore, awayscore, gamelength, utcmillis)
    print(match_data, home_team_data, away_team_data)


with open("./schedule_2016_03.json", encoding='utf8') as f:
    data = json.load(f)
    all_data = data["payload"]["dates"]
    for smy_data in all_data:
        group_data = smy_data["games"]
        for want_data in group_data:
            get_match_data(want_data)
