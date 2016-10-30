import urllib2
import json

from bs4 import BeautifulSoup

GP_URL = "http://www.gp.org/platform"

page = urllib2.urlopen(GP_URL).read()
soup = BeautifulSoup(page, "html.parser")

topics = []

for link in soup.find_all("a"):
    if "_2016/#" in link.get("href"):
        topics.append(link.getText())

with open('data/issues-green.json', 'w') as output:
    json.dump(topics, output, indent=2)
