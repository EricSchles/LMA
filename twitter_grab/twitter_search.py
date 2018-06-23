from TwitterSearch import TwitterSearchOrder, TwitterSearch
import pickle
import pandas as pd
from app.models import FAATwitter
from app import db

def add_creds(consumer_key,
              consumer_secret,
              access_token,
              access_token_secret):
    creds = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret,
        "access_token": access_token,
        "access_token_secret": access_token_secret
    }
    pickle.dump(creds, open("credentials.pkl", "wb"))

    
# add_creds(
#     consumer_key,
#     consumer_secret,
#     access_token,
#     access_token_secret
# )
creds = pickle.load(open("credentials.pkl", "rb"))

#top 30 airports:
#comes from here: https://en.wikipedia.org/wiki/List_of_the_busiest_airports_in_the_United_States
airports = [
    "ATL", "LAX", "ORD",
    "DFW", "DEN", "JFK",
    "SFO", "LAS", "SEA",
    "CLT", "MCO", "PHX",
    "MIA", "EWR", "IAH",
    "BOS", "MSP", "DTW",
    "PHL", "LGA", "FLL",
    "BWI", "DCA", "SLC",
    "MDW", "IAD","SAN",
    "TPA","PDX"
]
    
for airport in airports:    
    tso = TwitterSearchOrder()
    tso.set_keywords([airport])
    tso.set_language('en')
    tso.set_include_entities(False)

    ts = TwitterSearch(
        creds["consumer_key"],
        creds["consumer_secret"],
        creds["access_token"],
        creds["access_token_secret"]
    )

    for tweet in ts.search_tweets_iterable(tso):
        faa_tweet = FAATwitter(
            tweet["created_at"],
            tweet["text"],
            tweet["user"]["screen_name"]
        )
        db.session.add(faa_tweet)
        db.session.commit()
