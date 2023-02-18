import tweepy
from pandas import DataFrame

API_KEY = "SBy6atmEcUQWNItCfMZ0Ev9Ig"
API_SECRET = "sMRfuZRy3vvj7ctaIxggMcd6ZMZswsKf9phRD9fxZ5zLL1VHJz"

ACCESS_TOKEN = "739004328447475712-KgLW6zTwKXX160xy1C9w9bcxajb2e0n"
ACCESS_SECRET = "fSVZgx8NLpwlWdjM8pWqzC1xii7oQYPKH7pA8qp9C6BTS"

auth = tweepy.OAuth1UserHandler(
   API_KEY, API_SECRET,
   ACCESS_TOKEN, ACCESS_SECRET
)
api = tweepy.API(auth)

tweets = api.user_timeline(screen_name="Kandilli_info", 
                           count=200,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )

all_tweets = []
all_tweets.extend(tweets)
oldest_id = tweets[-1].id
while True:
    tweets = api.user_timeline(screen_name="Kandilli_info", 
                           count=200,
                           include_rts = False,
                           max_id = oldest_id - 1,
                           tweet_mode = 'extended'
                           )
    if len(tweets) == 0:
        break
    oldest_id = tweets[-1].id
    all_tweets.extend(tweets)
    print(f'Num of tweets downloaded till now {len(all_tweets)}')

dftweets =  [[tweet.id_str, 
             tweet.created_at, 
             tweet.favorite_count, 
             tweet.retweet_count, 
             tweet.full_text.encode("utf-8").decode("utf-8")] 
             for idx,tweet in enumerate(all_tweets)]

df = DataFrame(dftweets, columns=["id", "created_at", "favorite_count", "retweet_count", "text"])
df.to_csv('data/kandilli_tweets2.csv', index=False)