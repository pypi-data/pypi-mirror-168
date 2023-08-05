class Reply():
    def __init__(self, exclude_reply_user_ids: list[str], in_reply_to_tweet_id: str) -> None:
        self.exclude_reply_user_ids = exclude_reply_user_ids
        self.in_reply_to_tweet_id = in_reply_to_tweet_id

    def json(self):
        return {
            "exclude_reply_user_ids": self.exclude_reply_user_ids,
            "in_reply_to_tweet_id": self.in_reply_to_tweet_id
        }
