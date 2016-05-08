#!/usr/bin/env python3
# --*-- coding : utf-8 --*--

import sqlite3
import os
import re
from urllib.request import urlopen
import time
from urllib.error import URLError, HTTPError
import socket
socket.setdefaulttimeout(2)


# 全局变量
data_path = "/home/ji/pythonScripts/NBA/DATA/"
databasefile = data_path + "runcontrol.db"
datafile = data_path + "gamelist.txt"
gamedata_path = "/home/ji/pythonScripts/NBA/game_data/"
if not os.path.exists(data_path):
    os.mkdir(data_path)
if not os.path.exists(gamedata_path):
    os.mkdir(gamedata_path)


def insert_gameid():
    con = sqlite3.connect(databasefile)
    cur = con.cursor()
    cur.execute('create table if not exists gameid(id text PRIMARY KEY, isdone text)')
    cur.execute("delete from gameid")
    with open(datafile, 'r') as f:
        gameid = []
        for line in f:
            gameidtmp = re.split(r'\|\*\|', line)
            gameid.append(gameidtmp[0])
        gameid = list(set(gameid))
    for l in gameid:
        cur.execute('insert into gameid values (? ,?)', (l, 'N'))
    con.commit()
    con.close()


def get_game_data():
    con = sqlite3.connect(databasefile)
    cur = con.cursor()
    cur.execute("select id from gameid where isdone = 'N'")
    gameidlist = []
    for l in cur:
        gameidlist.append(l[0])
    for gameid in gameidlist:
        cur = con.cursor()
        cur.execute("select isdone from gameid where id = '"+gameid + "'")
        done_ornot = [l[0] for l in cur]
        if done_ornot == 'Y':
            pass
        else:
            gamedata_file = "game_" + gameid + ".json"
            print("getdata of "+gameid)
            try:
                with urlopen("http://china.nba.com/static/data/game/snapshot_" + gameid + ".json",
                             timeout=2) as respone:
                    with open(gamedata_path + gamedata_file, "w") as jsonfile:
                        jsonfile.write(respone.read().decode('utf-8'))
                    cur.execute("update gameid set isdone ='Y' where id = '" + gameid + "'")
                    con.commit()
            except URLError:
                continue
            except HTTPError:
                continue
            except socket.timeout:
                continue
        time.sleep(2)

get_game_data()






