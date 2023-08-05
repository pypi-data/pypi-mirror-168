from os import PathLike
from tweetipy.helpers.API import API_OAUTH_1_0_a
from tweetipy.handlers import HandlerTweets, HandlerMedia

class Tweetipy():
    def __init__(self,
        oauth_consumer_key: str, # TWITTER_API_KEY (App user)
        oauth_consumer_secret: str, # TWITTER_API_KEY_SECRET (App password)
        oauth_token: str = None, # TWITTER_ACCESS_TOKEN (Like the user or the user)
        oauth_token_secret: str = None, # TWITTER_ACCESS_TOKEN_SECRET (Like the password of the user)
        session_path: PathLike = None
    ) -> None:
        self._API = API_OAUTH_1_0_a(
            oauth_consumer_key,
            oauth_consumer_secret,
            oauth_token,
            oauth_token_secret,
            session_path
        )

    @property
    def tweets(self):
        return HandlerTweets(self._API)
    
    @property
    def media(self):
        return HandlerMedia(self._API)