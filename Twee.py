"""
Tweepy Documentation:
    https://tweepy.readthedocs.io/en/latest/
"""
import os
import re

import tweepy

from color_log.log_color import log_verbose, log_error, log_info


def twee():
    log_verbose("twee()")
    auth = tweepy.OAuthHandler(consumer_key=os.environ.get('TWEE_Consumer'),
                               consumer_secret=os.environ.get('TWEE_Consumer_secret'),
                               callback="twitter.com ")
    # TODO: user sing in
    # https://tweepy.readthedocs.io/en/latest/auth_tutorial.html
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError as er:
        log_error("\ttweepy.TweepError 1:\n%s" % er)
    # ....

    # AT THE MOMENT I USE MY personal keys
    auth.set_access_token(os.environ.get('TWEE_Access_token'), os.environ.get('TWEE_Access_token_secret'))

    api_twee = tweepy.API(auth)

    your_feed = []
    n_tweets = 20
    try:
        public_tweets = tweepy.Cursor(api_twee.home_timeline, tweet_mode='extended').items(n_tweets)

        for tweet in public_tweets:
            one_tweet = list()
            one_tweet.append(str(tweet.created_at))  # 0 * 5
            one_tweet.append(str(tweet.user.name))  # 1 * 5

            twit_ft = str(tweet.full_text)
            twit_end = re.search(r"https://", twit_ft)
            if twit_end:
                twit_end = twit_end.start(0)  # get index of a first met of 'https://'
                twit_text = twit_ft[:twit_end]
                one_tweet.append(twit_text)  # 2 * 5
            else:
                one_tweet.append(twit_ft)

            if 'media' in tweet.entities:
                one_tweet.append(str(tweet.entities['media'][0]['media_url_https']))  # 3 * 5
            else:
                one_tweet.append("")
            one_tweet.append(str(tweet.user.profile_image_url_https))  # 4 * 5

            reference = re.findall(r"https://\w+.\w+/\w+", twit_ft)
            if reference:
                one_tweet.append(reference[0])  # 5
                # log_warning("\ttwee() - reference %s" % reference)
            else:
                one_tweet.append("")  # 5
                # log_warning("\ttwee() - reference Not found")

            your_feed.append(one_tweet)
            # log_info(str(one_tweet))

    except tweepy.TweepError as er:
        log_error("\ttweepy.TweepError 2: \n%s" % er)

    if your_feed:
        log_info("\tload twee() - OK")
    else:
        log_error("\tError in twee()\nyour_feed = None")

    return your_feed


if __name__ == '__main__':
    twee()
