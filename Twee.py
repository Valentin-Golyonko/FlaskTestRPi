"""
Tweepy Documentation:
    https://tweepy.readthedocs.io/en/latest/
"""
import re

import tweepy

from MySteamListener_twee import MyStreamListener
from api_keys.keys import (access_token, consumer_secret, consumer_key, access_token_secret)
from color_log.log_color import log_verbose, log_error, log_info, log_warning


def twee():
    log_verbose("twee()")
    auth = tweepy.OAuthHandler(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               callback="twitter.com ")
    # TODO: user sing in
    # https://tweepy.readthedocs.io/en/latest/auth_tutorial.html
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError as er:
        log_error("\ttweepy.TweepError 1:\n%s" % er)
    # ....

    # AT THE MOMENT I USE MY personal keys
    auth.set_access_token(access_token, access_token_secret)

    api_twee = tweepy.API(auth)

    your_feed = []
    n_tweets = 20
    try:
        public_tweets = tweepy.Cursor(api_twee.home_timeline, tweet_mode='extended').items(n_tweets)

        for tweet in public_tweets:
            one_tweet = list()
            one_tweet.append(str(tweet.created_at))  # 0 * 5
            one_tweet.append(str(tweet.user.name))  # 1 * 5

            tft = str(tweet.full_text)
            text = re.search(r"", tft)

            one_tweet.append(str(tft))  # 2 * 5
            if 'media' in tweet.entities:
                one_tweet.append(str(tweet.entities['media'][0]['media_url_https']))  # 3 * 5
            else:
                one_tweet.append(str(""))
            one_tweet.append(str(tweet.user.profile_image_url_https))  # 4 * 5

            r = re.search(r"https://\w+.\w+/\w+", tft)
            if r:
                one_tweet.append(r.group(0))     # 5
            else:
                one_tweet.append("")  # 5

            your_feed.append(one_tweet)
            # log_info(str(one_tweet))

    except tweepy.TweepError as er:
        log_error("\ttweepy.TweepError 2: \n%s" % er)

    if your_feed:
        log_info("\tload twee() - OK")
    else:
        log_error("\tError in twee()\nyour_feed = None")

    return your_feed


def twee_stream():
    log_verbose("twee_stream()")
    auth = tweepy.OAuthHandler(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               callback="twitter.com ")
    auth.set_access_token(access_token, access_token_secret)
    api_twee = tweepy.API

    stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=api_twee, listener=stream_listener)

    my_stream.filter(track=['python'], is_async=True)


if __name__ == '__main__':
    # twee_stream()
    twee()
