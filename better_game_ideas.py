import json
import random

import twitter

def uniqify_preserve(mess):
    seen = {}
    result = []
    for item in mess:
        if item in seen:
            continue
        seen[item] = 1
        result.append(item)
    return result

ISSUE_SOURCES = [
    "data/issues-aclu.json",
    "data/issues-c4c-massaged.json",
    "data/issues-green.json",
]
GAMES_SOURCES = [
    "data/games-90-interesting.json"
]

TEMPLATES = [
    "What about a game like $$G but about $$I?",
    "A game in the style of $$G would be great for exploring $$I.",
    "Why are there no $$I games like $$G?",
    "$$G would have been more interesting if it explored $$I.",
    "Imagine a game like $$G crossed with $$G, but it's about $$I.",
    "Someone should make a $$G-alike around themes of $$I.",
    "$$G is a fascinating game, but misses opportunities to talk about $$I.",
    "The $$I community really should have a game like $$G",
    "A game about $$I, in the style of $$G... that could be something special.",
]

creds = json.load(open('credentials.json', 'r'))
twitterApi = twitter.Api(
                        creds['consumer-key'],
                        creds['consumer-secret'],
                        creds['access-token'],
                        creds['access-token-secret']
                        )

issues = []
for source in ISSUE_SOURCES:
    issue_list = json.load(open(source, 'r'))
    issues += issue_list

games  = []
for source in GAMES_SOURCES:
    game_list = json.load(open(source, 'r'))
    games += game_list

issues = uniqify_preserve(issues)
games = uniqify_preserve(games)

def lower_but_not_acronyms(text):
    ret = []
    has_acr = False
    for word in text.split():
        if word.isupper():
            ret.append(word)
        else:
            ret.append(word.lower())
    return " ".join(ret)

random.seed()
template = random.choice(TEMPLATES)
game_picks = random.sample(games, template.count("$$G"))
issue_picks = random.sample(issues, template.count("$$I"))
issue_picks = map(lower_but_not_acronyms, issue_picks)

text = template
text = text.replace("$$G", "%s") % tuple(game_picks)
text = text.replace("$$I", "%s") % tuple(issue_picks)

# print text
twitterApi.PostUpdate(text)