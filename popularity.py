import sys
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import json

consumer_key = '73SF0RGxn2qJOUwPTbEAxAfJs'
consumer_secret = 'bBfeyq01hodLQNe4uvymqaAeDMTGgKWaI1nTV49ReqlCFu208h'
access_token = '1552992276-RWHHNnjLtuoQLtmt3PL13dzRSQLIggtwisTfnSp'
access_secret = 'rxCohqZWqJUj36azXMLD2PL97t10NMnj5KX1TUzE3gzpO'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# for place in api.geo_search(lat=49.8397, long=24.0297, accuracy=10000):
# for place in tweepy.Cursor(api.search, count=1000, geocode="49.8397,24.0297,20km"):
# for place in api.search(count=1000, geocode="49.8397,24.0297,20km"):

# count = 0
# with open("places.json", mode="a") as file:
#     for place in tweepy.Cursor(api.search, count=100, geocode="49.8397,24.0297,20km", since_id=827018718790221824).items():
#
#         # Process a single status
#         if place.coordinates is not None:
#             count += 1
#             print(count)
#             file.write(json.dumps(place._json))
#             file.write("\n")
#
# print(count)

with open("places.json", 'r') as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        tweet = json.loads(line)
        if tweet['coordinates']:
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                    "text": tweet['text'],
                    "created_at": tweet['created_at']
                }
            }
            geo_data['features'].append(geo_json_feature)

# Save geo data
with open('geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))