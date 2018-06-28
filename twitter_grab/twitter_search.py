from TwitterSearch import TwitterSearchOrder, TwitterSearch
import pickle
import pandas as pd
from app.models import FAATwitter
from app import db
import time

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
airports = ['HPY', 'AZA', 'DWH', 'JFK', 'WSG', 'UKT', 'SKF', 'LDJ', 'SUU', 'HHR', 'RAL', 'AGC', 'POC', 'SMF', 'CDW', 'RND', 'LAX', 'CNO', 'BUR', 'CCB', 'HOU', 'FME', 'ABE', 'FOE', 'TCM', 'IWS', 'SWF', 'TIW', 'CGS', 'HIO', 'FUL', 'VNY', 'TMB', 'LGB', 'CSN', 'ANP', 'MIA', 'RDG', 'TTD', 'PHX', 'PWT', 'SEA', 'FRG', 'APG', 'MSC', 'TEB', 'ONT', 'POU', 'LGA', 'DAA', 'IAD', 'PIT', 'MHR', 'HPN', 'EMT', 'CTX', 'WHP', 'BRO', 'SGR', 'UGN', 'IAH', 'EWR', 'GAI', 'DPA', 'PPM', 'HWO', 'DXR', 'MCC', 'LJN', 'AUS', 'BWI', 'HRL', 'BFP', 'SMO', 'ORD', 'HCC', 'MEV', 'SAC', 'LWC', 'DCA', 'CPM', 'MYV', 'EFD', 'TVL', 'BFI', 'TOA', 'SHD', 'SCF', 'PWK', 'MNZ', 'SYR', 'SSF', 'FXE', 'PDX', 'DVT', 'RNT', 'HST', 'MDW', 'TOP', 'GYY', 'ISP', 'MMU', 'ADW', 'BTP', 'SAT', 'MGJ', 'SNA', 'HZL', 'ITH', 'FLL', 'PAE']

batch = []
for i in range(0, len(airports), 5):
    batch.append(airports[i:i+5])

for airports in batch:
    for airport in airports:    
        try:
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
        except:
            time.sleep(600)
    time.sleep(600)
