import urllib2
import json

from bs4 import BeautifulSoup

C4C_URL =  "https://educationforjustice.org/resource-maps-social-justice-topics"

page = urllib2.urlopen(C4C_URL).read()
soup = BeautifulSoup(page, "html.parser")

topics = []

for link in soup.find(id='content-area').find_all("a"):
    address = link.get('href')
    if address == None:
        continue

    if address.startswith("/node") or address.startswith("/principles-topics"):
        topics.append(link.getText())
    else:
        continue


for i in range(len(topics)):
    topic = topics[i]
    if topic.startswith("Rights - "):
        topics[i] = "%s Rights" % (topic[len("Rights - "):])

with open('data/issues-c4c.json', 'w') as output:
    json.dump(topics, output, indent=2)
