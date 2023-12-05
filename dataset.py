import pandas as pd

#creazione dataset twitter senza descrizioni
'''
twitter_tweet_collection = pd.read_csv("database/twitter/twitter_tweet_collection.csv")
twitter_users = pd.read_csv("database/twitter/twitter_users.csv")
twitter_tweet_hashtag = pd.read_csv("database/twitter/twitter_tweet_hashtag.csv")
twitter_tweets = pd.read_csv("database/twitter/twitter_tweets.csv")
    
# unisci il dataset
merged_data = pd.merge(twitter_tweets, twitter_tweet_collection, on="tweet_id")
merged_data = pd.merge(merged_data, twitter_users, left_on="author_id", right_on="user_id")
merged_data = pd.merge(merged_data, twitter_tweet_hashtag, on="tweet_id")
    
final_data = merged_data[["user_id", "tweet_id", "collection", "hashtag", "created_at", "author_id", "retweet_count", "reply_count", "like_count", "quote_count"]]
#bisogna poi mettere anche i campi "content" e "user_id" per avere il merged completo e fare una ricerca sul contenuto dei tweet

# salvalo
final_data.to_csv("merged_twitter_data.csv", index=False) 
'''


