class Tweet():
    def __init__(self, id: str, text: str) -> None:
        self._id = id
        self._text = text
    
    @property
    def id(self):
        return self._id
    
    @property
    def text(self):
        return self._text
    
    def json(self):
        return {
            "id": self.id,
            "text": self.text
        }

    def __str__(self) -> str:
        return str(self.json())