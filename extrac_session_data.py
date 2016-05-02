#!/usr/bin/env python3
# coding = utf-8
import json
import sqlite3
import os


# 处理客队或者主队的数据
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
    isallstarteam = profile["isAllStarTeam"]
    isleagueteam = profile["isLeagueTeam"]
    name = profile["name"]
    nameen = profile["nameEn"]

    return (confrank, divrank, losses, abbr, city, cityen, code, conference, displayabbr,
            displayconference, division, isallstarteam, isleagueteam, name, nameen)


# 解析每场比赛的公共数据（出场人数,比分等）
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
    awayteam_data = get_team_data(in_data["awayTeam"])
    hometeam_data = get_team_data(in_data["homeTeam"])
    match_data = (gameid, hometeamid, awayteamid, seasontype, arenalocation, arenaname,
                  attendance, homescore, awayscore, gamelength, utcmillis)
    sum_data = match_data+hometeam_data+awayteam_data
    with open(datafile_for_load, "at") as file:
        for i in range(len(sum_data)):
            if i != len(sum_data)-1:
                file.write(str(sum_data[i]))
                file.write("|*|")
            else:
                file.write(str(sum_data[i]))
        file.write("\n")


# 将每场比赛的数据追加写入数据文件,等待向数据库中加载
def extrac_json(json_file):
    with open(json_file, encoding='utf8') as f:
        data = json.load(f)
        all_data = data["payload"]["dates"]
        for smy_data in all_data:
            group_data = smy_data["games"]
            for want_data in group_data:
                get_match_data(want_data)


# 调用sqlite3,传入sql和附带数据,返回执行结果,ddl语句及upd语句正常执行后返回[]
def run_sql(database, sql_str, insert_data=None):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if insert_data is None:
        cur.execute(sql_str)
    else:
        cur.execute(sql_str, insert_data)
    reslut = []
    for l in cur:
        reslut.append(l)
    con.commit()
    con.close()
    return reslut


# 建立流程控制表并插入文件列表,防止数据文件多次被处理
def create_con_table(path):
    create_table_sql = "create table if not exists extrac_json(filename text, isdone text)"
    insert_data = "insert into extrac_json values (?, ?)"
    run_sql(databasefile, create_table_sql)
    filelist = os.listdir(path)
    for filename in filelist:
        run_sql(databasefile, insert_data, (filename, 'N'))


# 更新流程控制表中文件处理的状态为已处理
def upd_isdone(filename):
    upd_sql = "update extrac_json set isdone = ? where filename = ?"
    run_sql(databasefile, upd_sql, ('Y', filename))


# 获取流程控制表中文件处理状态
def get_isdone(filename):
    sel_sql = "select isdone from extrac_json where filename = ? "
    isdone = run_sql(databasefile, sel_sql, (filename,))
    return isdone[0][0]

# 全局变量
session_data_path = "/home/ji/pythonScripts/NBA/session_data/"
data_path = "/home/ji/pythonScripts/NBA/DATA/"
databasefile = data_path + "runcontrol.db"
datafile_for_load = data_path + "gamelist.txt"
if not os.path.exists(data_path):
    os.mkdir(data_path)


# 初始化函数
def begin_again():
    if os.path.exists(databasefile):
        os.remove(databasefile)
    if os.path.exists(datafile_for_load):
        os.remove(datafile_for_load)


def main():
    create_con_table(session_data_path)
    session_files = os.listdir(session_data_path)
    for sessionfile in session_files:
        doneornot = get_isdone(sessionfile)
        if doneornot != 'Y':
            extrac_json(session_data_path+'/'+sessionfile)
            upd_isdone(sessionfile)
        else:
            continue


# 初始化,从新解析
# begin_again()

main()

