#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

import os
import sqlite3


i = os.listdir("../session_data/")
# for l in i:
#     print(l)


con = sqlite3.connect("/home/ji/pythonScripts/NBA/tmp.db")

cl = con.cursor()

cl.execute("create table if not exists tmp(filename text, isdone text) ")


for filename in i:
    cl.execute("insert into tmp values (?, ?)", (filename, 'N'))

con.commit()


