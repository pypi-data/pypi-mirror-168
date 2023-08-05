from typing import Literal


class Scope():
    ScopeLevel = Literal["read", "write"]
    ScopeCanReadOnly = Literal["read"]
    def __init__(self,
        tweet: ScopeLevel = None,
        users: ScopeCanReadOnly = None,
        follows: ScopeLevel = None,
        spaces: ScopeCanReadOnly = False,
        mute: ScopeLevel = None,
        like: ScopeLevel = None,
        lists: ScopeLevel = None,
        block: ScopeLevel = None,
        bookmark: ScopeLevel = None,
        tweet_moderate: bool = False,
        offline_access: bool = False,
    ) -> None:
        # See "Scopes" section under:
        # https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code

        self._regular_scopes = {
            "tweet": tweet,
            "users": users, # This one can -at most- read.
            "follows": follows,
            "spaces": spaces, # This one can -at most- read.
            "mute": mute,
            "like": like,
            "list": lists,
            "block": block,
            "bookmark": bookmark
        }

        # Special scopes
        self._tweet_moderate = tweet_moderate
        self._offline_access = offline_access
    
    def string(self):
        scopes = []

        # Regular scopes
        for scope, level in self._regular_scopes.items():
            if level == "write":
                scopes.extend([
                    f"{scope}.read",
                    f"{scope}.write"
                ])
            if level == "read":
                scopes.append(f"{scope}.read")
        
        # Special scopes
        if self._tweet_moderate == True:
            # Hide and unhide replies to your Tweets.
            scopes.append('tweet.moderate.write')
        if self._offline_access == True:
            # Stay connected to your account until you revoke access.
            scopes.append('offline.access')
        return "20%".join(scopes)
