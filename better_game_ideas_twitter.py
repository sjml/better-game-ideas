import json
import os

import twitter

from better_game_ideas import makeGamePitch

os.chdir(os.path.dirname(os.path.realpath(__file__)))

creds = json.load(open('credentials.json', 'r'))
twitterApi = twitter.Api(
                        creds['consumer-key'],
                        creds['consumer-secret'],
                        creds['access-token'],
                        creds['access-token-secret']
                        )

try:
    twitterApi.PostUpdate(makeGamePitch()[0])
except Exception as e:
    pass # just silently fail if something goes wrong; this script is in no way mission critical)
