#!/usr/bin/env python3
# coding : utf-8

from urllib.request import urlopen
import os
import time


def get_url_list():
    base_url = "http://china.nba.com/static/data/season/schedule_"
    url_list = [(base_url + str(2000 + m).zfill(2) + "_" + str(n + 1).zfill(2) + ".json")
                for m in range(17) for n in range(12)]
    return url_list


def get_json_file(url_list, path):
    for url in url_list:
        filename = url[url.index("schedule"):]
        with urlopen(url) as response:
            print(filename)
            while not os.path.exists(path+filename):
                with open(path+filename, 'w') as json_file:
                    json_file.write(response.read().decode('utf8'))
        time.sleep(3)
        # break


def main():
    data_path = os.getcwd()+'/session_date/'
    url_list = get_url_list()
    while not os.path.exists(data_path):
        os.mkdir(data_path)
    get_json_file(url_list, data_path)


main()

