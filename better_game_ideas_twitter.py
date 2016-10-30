import json

import twitter

from better_game_ideas import makeGamePitch

creds = json.load(open('credentials.json', 'r'))
twitterApi = twitter.Api(
                        creds['consumer-key'],
                        creds['consumer-secret'],
                        creds['access-token'],
                        creds['access-token-secret']
                        )

twitterApi.PostUpdate(makeGamePitch()[0])
