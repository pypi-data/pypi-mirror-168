from typing import Literal
from tweetipy.helpers.API import API_OAUTH_1_0_a
from tweetipy.types import Media, Poll, Reply, Tweet


class HandlerTweets():

    ReplySettings = Literal["mentionedUsers", "following"]

    def __init__(self, API: API_OAUTH_1_0_a) -> None:
        self.API = API

    def write(
        self,
        # media, poll and quote_tweet_id are mutually exclusive
        direct_message_deep_link: str = None,
        for_super_followers_only: bool = None,
        media: Media = None,
        poll: Poll = None,
        quote_tweet_id: str = None,
        reply: Reply = None,
        reply_settings: ReplySettings = None,
        text: str = None  # Required if media not present
    ):
        endpoint = 'https://api.twitter.com/2/tweets'

        # body logic ---------------------------------------------------------
        if (media != None) + (poll != None) + (quote_tweet_id != None) > 1:
            raise Exception(
                "media, poll and quote_tweet_id are mutually exclusive. This means you can only use one of them at the same time.")
        if media == None and text == None:
            raise Exception(
                "text argument is required if no media is present.")
        # ----------------------------------------------------------------------

        body = {
            "media": media.json() if media != None else None,
            "poll": poll.json() if poll != None else None,
            "quote_tweet_id": quote_tweet_id,
            "direct_message_deep_link": direct_message_deep_link,
            "for_super_followers_only": for_super_followers_only,
            "reply": reply.json() if reply != None else None,
            "reply_settings": reply_settings,
            "text": text,
        }

        # Remove unused params -------------------------------------------------
        clean_body = {}
        for key, val in body.items():
            if val != None:
                clean_body[key] = val
        body = clean_body.copy()
        # ----------------------------------------------------------------------

        r = self.API.post(url=endpoint, json=body)
        if r.status_code == 201:
            return Tweet(**r.json()["data"])
        else:
            print(r.text)
            r.raise_for_status()
