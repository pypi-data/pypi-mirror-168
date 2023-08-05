import json
from os import PathLike
from requests_oauthlib import OAuth1, OAuth1Session
from requests import Request, Response, Session
from urllib.parse import urlencode
from typing import Literal


class API_OAUTH_1_0_a():

    def authorize(self, force: bool = False) -> OAuth1:
        if self.oauth_token != None and self.oauth_token_secret != None:
            return OAuth1(
                self.oauth_consumer_key,
                client_secret=self.oauth_consumer_secret,
                resource_owner_key=self.oauth_token,
                resource_owner_secret=self.oauth_token_secret)
        else:
            if force == False:
                # Try to use existing session
                try:
                    with open(self.session_path, 'r', encoding='utf-8') as s:
                        session = json.load(s)
                        return OAuth1(
                            self.oauth_consumer_key,
                            client_secret=self.oauth_consumer_secret,
                            resource_owner_key=session["oauth_token"],
                            resource_owner_secret=session["oauth_token_secret"]
                        )
                except (KeyError, FileNotFoundError):
                    # Session is not available, so we continue with regular
                    # authorization flow
                    pass
            # Regular authorization flow
            request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
            oauth = OAuth1Session(
                self.oauth_consumer_key,
                client_secret=self.oauth_consumer_secret)

            try:
                fetch_response = oauth.fetch_request_token(request_token_url)
            except ValueError:
                print("There may have been an issue with the consumer_key or consumer_secret you entered.")

            resource_owner_key = fetch_response.get("oauth_token")
            resource_owner_secret = fetch_response.get("oauth_token_secret")
            print("Got OAuth token: %s" % resource_owner_key)

            # Get authorization
            base_authorization_url = "https://api.twitter.com/oauth/authorize"
            authorization_url = oauth.authorization_url(base_authorization_url)
            print("Please go here and authorize: %s" % authorization_url)
            verifier = input("Paste the PIN here: ")

            # Get the access token
            access_token_url = "https://api.twitter.com/oauth/access_token"

            oauth = OAuth1Session(
                self.oauth_consumer_key,
                client_secret=self.oauth_consumer_secret,
                resource_owner_key=resource_owner_key,
                resource_owner_secret=resource_owner_secret,
                verifier=verifier,
            )
            oauth_tokens = oauth.fetch_access_token(access_token_url)

            access_token = oauth_tokens["oauth_token"]
            access_token_secret = oauth_tokens["oauth_token_secret"]
            session = {
                "oauth_token": access_token,
                "oauth_token_secret": access_token_secret,
                "user_id": oauth_tokens["user_id"],
                "screen_name": oauth_tokens['screen_name']
            }
            with open(self.session_path, 'w', encoding='utf-8') as s:
                json.dump(session, s)

            return OAuth1(
                client_key=self.oauth_consumer_key,
                client_secret=self.oauth_consumer_secret,
                resource_owner_key=access_token,
                resource_owner_secret=access_token_secret)

    def __init__(self, oauth_consumer_key: str, oauth_consumer_secret: str, oauth_token: str = None, oauth_token_secret: str = None, session_path: PathLike = None) -> None:
        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_consumer_secret = oauth_consumer_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.session_path = session_path if session_path != None else 'session.json'
        self.oauth = self.authorize()

    _Methods = Literal["GET", "POST", "PUT", "DELETE"]

    def _percent_encode(self, string: str) -> str:
        return urlencode({'x': string})[2:]

    def _req(self, method: _Methods, url: str, params: dict = None, json: dict = None, files: dict = None) -> Response:
        req = Request(
            method=method,
            url=url,
            params=params,
            json=json,
            auth=self.oauth,
            files=files
        )
        prepped = req.prepare()
        with Session() as session:
            res = session.send(prepped)
            return res

    def get(self, url: str, params: dict = None, json: dict = None) -> Response:
        return self._req("GET", url=url, params=params, json=json)

    def post(self, url: str, params: dict = None, json: dict = None, files: dict = None) -> Response:
        return self._req("POST", url=url, params=params, json=json, files=files)

    def put(self, url: str, params: dict = None, json: dict = None) -> Response:
        return self._req("PUT", url=url, params=params, json=json)

    def delete(self, url: str, params: dict = None, json: dict = None) -> Response:
        return self._req("DELETE", url=url, params=params, json=json)
