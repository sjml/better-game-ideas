import json

METASCORE_CUTOFF = 90

# we don't need fancy regex to recognize all of them; just the ones
#  most likely to see in a game title
ROMAN_NUMERALS = [
    "I", "II", "III", "IV", "V",
    "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV",
    "XVI", "XVII", "XVIII", "XIX", "XX"
]

raw_popular = json.load(open("data/games-raw-%d.json" % METASCORE_CUTOFF, "r"))
raw_interesting = json.load(open("data/games-raw-interesting.json", "r"))

raw_titles = []
processed_titles = []

possible_series = {}

for system, games in raw_popular.iteritems():
    for game in games:
        raw_titles.append(game)
for year in raw_interesting.keys():
    for system, games in raw_interesting[year].iteritems():
        for game in games:
            raw_titles.append(game)

for title in raw_titles:
    rerelease_indicators = [
        "Edition",
        "Collection",
        "Remix",
        " HD",
        " 3D",
    ]
    if any(ri in title for ri in rerelease_indicators):
        # don't care
        continue

    # strip out "Episode" bits
    col_split = title.split(":")
    if len(col_split) > 1 and "episode" in col_split[-1].lower():
        title = col_split[0]

    # do I contain numbers at the end?
    if (title.split()[-1].isdigit()):
        # unless it's all after a colon
        if not title.split(':')[-1].strip().isdigit():
            processed_titles.append(' '.join(title.split()[:-1]))
            continue

    # is there a dash?
    if " - " in title:
        title = title.split(" - ")[0]

    # remove vanity titling
    title = title.replace("Tom Clancy's ", "")

    # is there a colon?
    if ":" in title:
        split = title.split(":")
        # special case special games :)
        if "Elder Scrolls" in title:
            processed_titles.append(split[1])
            continue
        if "Legend of Zelda" in title:
            processed_titles.append(split[1])
            continue
        if "Spider:  The Secret of Bryce Manor" == title:
            # special case AND fix typo for my friend's game :D
            processed_titles.append("Spider: The Secret of Bryce Manor")
            continue
        if "Spider: The Secret of the Shrouded Moon" == title:
            processed_titles.append(title)
            continue

        if (split[0].split()[-1].isdigit()):
            # number before colon, like Uncharted 2: Among Thieves
            #  probably is called by the pre-colon title
            processed_titles.append(split[0])
            continue
        elif any(rn == split[0].split()[-1] for rn in ROMAN_NUMERALS):
            # same for roman numerals
            processed_titles.append(split[0])
            continue
        else:
            # throw it out to later processing
            if split[0] not in possible_series.keys():
                possible_series[split[0]] = []
            possible_series[split[0]].append(split[1])
            continue

    # a normal title
    processed_titles.append(title)

def uniqify_preserve(mess):
    seen = {}
    result = []
    for item in mess:
        if item in seen:
            continue
        seen[item] = 1
        result.append(item)
    return result

# check for series
for series, entries in possible_series.iteritems():
    # only one, we probably just call by pre-colon name
    entries = uniqify_preserve(entries)
    if len(entries) == 1:
        processed_titles.append(series)
        continue

    # works pretty well to just pick the first (higher-rated, most likely) entry
    processed_titles.append("%s:%s" % (series, entries[0]))


titles = uniqify_preserve(processed_titles)
titles = map(str, titles)
titles = map(str.strip, titles)

with open('data/games-%d-interesting.json' % METASCORE_CUTOFF, 'w') as output:
    json.dump(titles, output, indent=2)
