class Media():
    def __init__(self, media_ids: list[str], tagged_user_ids: list[str] = None) -> None:
        self.media_ids = media_ids
        self.tagged_user_ids = tagged_user_ids
    
    def json(self):
        media_json = {"media_ids": self.media_ids}
        if self.tagged_user_ids == None:
            return media_json
        else:
            media_json["tagged_user_ids"] = self.tagged_user_ids
            return media_json
