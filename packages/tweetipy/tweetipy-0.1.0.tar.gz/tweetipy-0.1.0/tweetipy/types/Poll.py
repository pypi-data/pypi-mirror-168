class Poll():
    def __init__(self, options: list[str], duration_minutes: int) -> None:
        self.options = options
        self.duration_minutes = duration_minutes
    
    def json(self):
        return {
            "options": self.options,
            "duration_minutes": self.duration_minutes
        }
