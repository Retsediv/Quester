import tweepy
from tweepy import OAuthHandler

consumer_key = '73SF0RGxn2qJOUwPTbEAxAfJs'
consumer_secret = 'bBfeyq01hodLQNe4uvymqaAeDMTGgKWaI1nTV49ReqlCFu208h'
access_token = '1552992276-RWHHNnjLtuoQLtmt3PL13dzRSQLIggtwisTfnSp'
access_secret = 'rxCohqZWqJUj36azXMLD2PL97t10NMnj5KX1TUzE3gzpO'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)