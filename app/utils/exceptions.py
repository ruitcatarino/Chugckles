class GameFinished(Exception):
    def __init__(self, message="Game is already finished"):
        self.message = message
        super().__init__(self.message)