#!coding = utf-8
import json
from pprint import pprint


with open("./schedule_2016_03.json", encoding='utf8') as f:
    data = json.load(f)

pprint(data)
