from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import time
import twitter_credentials
import re
import numpy as np
import pandas as pd
import json


####Authenticator
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        auth.set_access_token(twitter_credentials.access_token_key, twitter_credentials.access_token_secret)
        return auth



class TwitterStreamer():
        '''
        Class for streaming and processing tweets
        '''
        def __init__(self):
            self.twitter_authenticator = TwitterAuthenticator()
            pass

        def stream_tweets(self, fetched_tweets_filename, data_for_capture):
            # This handles Twitter Authentication and connection to Streaming Api
            listener = TwitterListener(fetched_tweets_filename)
            auth = self.twitter_authenticator.authenticate_twitter_app()
            stream = Stream(auth, listener)
            # Line filter Twitter Streams to Capture
            stream.filter(track=data_for_capture)


##StreamListener
class TwitterListener(StreamListener):
    '''
    Prints received tweets to stdout
    '''
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename


    def on_data(self, raw_data):
        try:

            data = json.loads(raw_data)
            if 'retweeted_status' in data:
                if 'extended_tweet' in data['retweeted_status']:
                    if 'full_text' in data['retweeted_status']['extended_tweet']:
                        txt = data['retweeted_status']['extended_tweet']['full_text']
                    else:
                        txt = data['retweeted_status']['text']
                else:
                    txt = data['retweeted_status']['text']
            elif 'extended_tweet' in data:
                if 'full_text' in data['extended_tweet']:
                    txt = data['extended_tweet']['full_text']
                else:
                    txt = data['text']
            else:
                txt = data['text']
            print(txt)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(json.dumps({'timestamp': data['created_at'],
                                     'tweet': txt})
                         )
                tf.write("\n\n--- NEW TWEET  ---\n\n")
            return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returns False on data_method in case rate limit occurs
            return False
        print(status)


if __name__ == "__main__":
    data_for_capture = ["Book of Matthew", "Gospel of Matthew", " -Matthew ", "Matthew KJV", "Matthew NIV", "Matthew NRSV", "Matthew NAB",
                        "Matthew TLB", "Matthew RSV", "Matthew NKJV", "Matthew ESV",



                        "Book of Mark", "Gospel of Mark", " -Mark ", "Mark KJV", "Mark NKJV", "Mark ESV", "Mark NIV", "Mark NRSV", "Mark NAB",
                        "Mark TLB", "Mark RSV",



                        "Book of Luke","Gospel of luke", " -luke ", "luke KJV", "Luke NKJV", "Luke ESV", "luke NIV", "luke NRSV", "luke NAB",
                        "luke TLB", "luke RSV",



                        "book of John", "Gospel of John", " -John ", "John KJV", "John NKJV", "John ESV", "John NIV", "John NRSV", "John NAB",
                        "John TLB", "John RSV",

                        " Acts of the Apostles", "-Apostles", "-Acts" "Acts KJV", "Acts NKJV", "Acts ESV", "Acts NIV", "Acts NRSV", "Acts NAB",
                        "Acts TLB", "Acts RSV",

                        "Book of Romans", "-Romans", "Romans KJV", "Romans NKJV", "Romans ESV", "Romans NIV", "Romans NRSV", "Romans NAB",
                        "Romans TLB", "Romans RSV",



                        "First Epistle to the Corinthians", "First Corinthians", "-Corinthians", "Corinthians NKJV", "Corinthians ESV",
                        "Corinthians KJV", "Corinthians NIV", "Corinthians NRSV", "Corinthians NAB", "Corinthians TLB", "Corinthians RSV", #"1 Corinthians",
                        "Second Epistle to the Corinthians", "Second Corinthians", #"2 Corinthians",

                        " Galatians", " Ephesians", " Philippians", " Colossians", "1 Thessalonians", "2 Thessalonians", "Philemon",


                        "First Epistle to Timothy", "First Timothy", "-Timothy", "Timothy KJV", "Timothy NKJV", "Timothy ESV", "Timothy NIV",
                        "Timothy NRSV", "Timothy NAB", "Timothy TLB", "Timothy RSV",



                        "Second Epistle to Timothy", "Second Timothy", #""2 Timothy",

                        "Epistle to Titus", "Epistle of Paul to Titus", " -Titus" "Titus KJV", "Titus NKJV", "Titus ESV", "Titus NIV",
                        "Titus NRSV", "Titus NAB", "Titus TLB", "Titus RSV",#"titus",



                        "Epistle to the Hebrews", "Letter to the Hebrews", "-Hebrews", "Hebrews KJV", "Hebrews NKJV", "Hebrews ESV",
                        "Hebrews NIV", "Hebrews NRSV", "Hebrews NAB", "Hebrews TLB", "Hebrews RSV",



                        "Epistle of James", "-James", "James KJV", "James NKJV", "James ESV", "James NIV", "James NRSV", "James NAB",
                        "James TLB", "James RSV",


                        "First Epistle of Peter",  "First Peter", "-Peter", "Peter KJV", "Peter NKJV", "Peter ESV", "Peter NIV",
                        "Peter NRSV", "Peter NAB", "Peter TLB", "Peter RSV", #"1 Peter",
                        "Second Epistle of Peter", "Second Peter", #"2 Peter",


                        "First Epistle of John", #"First John", #"1 John", "I John",
                        "Second Epistle of John", #"Second John", #" 2 John", "II John",
                        "Third Epistle of John", "Third John", #"3 John", "III John",



                        "Epistle of Jude", "-Jude" "Jude KJV", "Jude NIV", "Jude NRSV", "Jude NAB", "Jude TLB", "Jude RSV", "Jude NKJV", "Jude ESV",


                        "Book of Revelation", "-Revelation" "Revelation KJV", "Revelation NKJV", "Revelation ESV", "Revelation NIV", "Revelation NRSV", "Revelation NAB", "Revelation TLB", "Revelation RSV"
                        ]


    fetched_tweets_filename = "tweets.txt"
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, data_for_capture)

    # while elapsed <= 28800: #86400 24 hrs
    #     start = time.time()
    #     elapsed = 0
    #     elapsed = time.time() - start
    #
    #     print("Time's up!")

#python time limit





    #twitter_client = TwitterClient()
    #tweet_analyzer = TweetAnalysis()

    #api = twitter_client.get_twitter_client_api()

    #tweets = api.user_timeline(screen_name="jonapello", count=20)

    #df = tweet_analyzer.tweets_to_data_frame(tweets)




    #print(df.head(10))




    #api = twitter_client.get_twitter_client_api()

    #tweets = api.user_timeline

    #get most liked tweet of batch
    #print(np.max(df['likes']))

    # Time Series
    #time_likes = pd.Series(data=df['likes'].values, index=df['date'])
   # time_likes.plot(figsize=(16, 4), label="likes", legend=True)

   # time_likes = pd.Series(data=df['id'].values, index=df['date'])
   # time_likes.plot(figsize=(16, 4), label="id", legend=True)

  #  plt.show()


# class TwitterClient():
#     def __init__(self, twitter_user=None):
#         self.auth = TwitterAuthenticator().authenticate_twitter_app()
#         self.twitter_client = API(self.auth)
#
#         self.twitter_user = twitter_user
#
#
#     def get_twitter_client_api(self):
#         return self.twitter_client
#
#     def get_user_timeline_tweets(self, num_tweets):
#         tweets = []
#         for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
#             tweets.append(tweet)
#         return tweets
#
#     def get_friend_list(self, num_friends):
#         friend_list = []
#         for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
#             friend_list.append(friend)
#         return friend_list
#
#     def get_home_timeline_tweets(self, num_tweets):
#         home_timeline_tweets = []
#         for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
#             home_timeline_tweets.append(tweet)
#         return home_timeline_tweets