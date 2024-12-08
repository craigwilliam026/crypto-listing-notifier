import tweepy

# Twitter API credentials
consumer_key = 'GyWwycS6U8pk2VvwPwr0itsa1'
consumer_secret = 'mr5yvX4k7bmhCxeQHtxPVjyasQaMeVdgOIO5h2lnV1RWUPxNkx'
access_token = '1495991855032713219-ePsJArOAdzD5rvCl4C43CZGrtwTVvi'
access_token_secret = 'kLnAqAhS9r96neMLAOSDG6cynjDENMrKwJsFK5j4nNQR6'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def check_for_announcements():
    # Search for tweets from Binance announcing new listings
    for tweet in api.search(q="Binance will list", count=10):
        print(f"New listing announced: {tweet.text}")

check_for_announcements()
