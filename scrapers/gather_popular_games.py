import json
import time
import random
import sys

import requests
from bs4 import BeautifulSoup

METASCORE_CUTOFF = 90
METACRITIC_CURRENT_LIST_URL = "http://www.metacritic.com/browse/games/score/metascore/all/%s/filtered?sort=desc"
METACRITIC_CURRENT_SYSTEMS = [
    "ps3",
    "ps4",
    "ios",
    "vita",
    "3ds",
    "wii-u",
    "pc",
    "xbox360",
    "xboxone",
]
METACRITIC_LEGACY_LIST_URL = "http://www.metacritic.com/browse/games/release-date/available/%s/metascore"
METACRITIC_LEGACY_SYSTEMS = [
    "dreamcast",
    "psp",
    "gba",
    "n64",
    "gamecube",
    "ds",
    "wii",
    "xbox",
    "ps",
    "ps2",
    "ps2",
]


random.seed()
titles = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

for system in METACRITIC_LEGACY_SYSTEMS:
    print "Fetching data for %s" % system
    titles[system] = []
    url = METACRITIC_LEGACY_LIST_URL % system
    response = requests.get(url, headers=headers)
    raw_page = response.content

    soup = BeautifulSoup(raw_page, "html.parser")
    for game in soup.find_all("div", "product_wrap"):
        title = game.find("a").getText().strip()
        score = int(game.find("div", "metascore_w").getText().strip())
        if (score >= METASCORE_CUTOFF):
            titles[system].append(title)

    time.sleep(random.uniform(1.5, 7.0))


for system in METACRITIC_CURRENT_SYSTEMS:
    print "Fetching data for %s" % system
    titles[system] = []
    url = METACRITIC_CURRENT_LIST_URL % system
    response = requests.get(url, headers=headers)
    raw_page = response.content

    soup = BeautifulSoup(raw_page, "html.parser")
    for game in soup.find_all("div", "product_row"):
        title = game.find("a").getText().strip()
        score = int(game.find("div", "metascore_w").getText().strip())
        if (score >= METASCORE_CUTOFF):
            titles[system].append(title)

    time.sleep(random.uniform(1.5, 7.0))


with open('data/games-raw-%d.json' % METASCORE_CUTOFF, 'w') as output:
    json.dump(titles, output, indent=2)
