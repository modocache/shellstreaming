# -*- coding: utf-8 -*-
from nose.tools import *
from os.path import abspath, dirname, join, exists
from shellstreaming.config import Config
from shellstreaming.inputstream.tweet import Tweet


def test_tweet_usage():
    # To fully pass this test, create 'shellstreaming/test/data/shellstreaming_test_tweet.cnf' whose contents are:
    #
    # [inputstream.tweet]
    # consumer_key = <your consumer key>
    # consumer_secret = <your consumer secret>
    # access_token = <your access token>
    # access_token_secret = <your access token secret>
    # public_tweets_url = https://stream.twitter.com/1.1/statuses/sample.json
    #
    confpath = join(abspath(dirname(__file__)), '..', 'data', 'shellstreaming_test_tweet.cnf')
    if not exists(confpath):
        return

    config = Config.instance()
    config.set_config_file(confpath)

    n_batches = 5
    stream = Tweet(
        # [todo] - use config for not showing my keys & secrets
        consumer_key=config.get('inputstream.tweet', 'consumer_key'),
        consumer_secret=config.get('inputstream.tweet', 'consumer_secret'),
        access_token=config.get('inputstream.tweet', 'access_token'),
        access_token_secret=config.get('inputstream.tweet', 'access_token_secret'),

        batch_span_ms=1000,
    )
    for i_batch, batch in enumerate(stream):
        print(batch)
        n_batches -= 1
        if n_batches == 0:
            stream.interrupt()
