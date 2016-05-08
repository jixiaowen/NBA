#!/usr/bin/env python3
# --*-- coding :utf8 --*--

import sqlite3
import os


def run_sql(databasefile, sql_str, insert_data=None):
    con = sqlite3.connect(databasefile)
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

database_file = "/home/ji/pythonScripts/NBA/DATA/runcontrol.db"
create_sql = "create table if not exists tmp(filename text, isdone text)"
insert_sql = "insert into tmp values (?, ?)"
sel_sql = "select count(*) from gameid where isdone = 'Y'"
upd_sql = "update extrac_json set isdone = ? where filename = ?"
sel_isdone = "select isdone from extrac_json where filename = ? "
del_sql = 'delete from gameid'
drop_sql = 'drop table gameid'


# run_sql(database_file, upd_sql, ('N',))

# m = run_sql(database_file, sel_isdone, ('schedule_2009_09.json',))
# print(m)

# run_sql(database_file, del_sql)

l = run_sql(database_file, sel_sql)
for i in l:
    print(i)

# run_sql(database_file, drop_sql)



# filelist = os.listdir("/home/ji/pythonScripts/NBA/session_data/")
# for filename in filelist:
#     run_sql(insert_sql, (filename, 'N'))
