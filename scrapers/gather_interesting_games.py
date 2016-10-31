import json
import time
import datetime

import random
import sys

import requests
from bs4 import BeautifulSoup

METASCORE_DISCUSSION_CUTOFF = 100
METACRITIC_DISCUSS_URL = "http://www.metacritic.com/browse/games/score/metascore/discussed/%s/filtered?sort=desc&year_selected=%d"
METACRITIC_CURRENT_SYSTEMS = [
    ("ps3", 2006),
    ("ps4", 2013),
    ("ios", 2007),
    # ("vita", 2011), # gives too much weird stuff
    ("3ds", 2011),
    ("wii-u", 2012),
    ("pc", 1995),
    ("xbox360", 2005),
    ("xboxone", 2013),
]


random.seed()
titles = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

for year in range(1995, datetime.datetime.now().year + 1):
    print "Fetching data for the year %d" % year
    titles[year] = {}
    for systemData in METACRITIC_CURRENT_SYSTEMS:
        if systemData[1] > year:
            continue
        system = systemData[0]
        print "\tFetching data for %s" % system
        titles[year][system] = []
        url = METACRITIC_DISCUSS_URL % (system, year)
        response = requests.get(url, headers=headers)
        raw_page = response.content

        soup = BeautifulSoup(raw_page, "html.parser")
        count = 0
        for game in soup.find_all("div", "product_row"):
            count += 1
            title = game.find("a").getText().strip()
            discussionsTXT = game.find("div", "product_review_count_txt").getText().strip()
            discussions = int(discussionsTXT.split()[0])
            if (discussions >= METASCORE_DISCUSSION_CUTOFF):
                titles[year][system].append(title)
            elif (count <= 10):
                titles[year][system].append(title)
            else:
                break

        if len(titles[year][system]) == 0:
            del titles[year][system]

        time.sleep(random.uniform(1.5, 7.0))


with open('data/games-raw-interesting.json', 'w') as output:
    json.dump(titles, output, indent=2)
