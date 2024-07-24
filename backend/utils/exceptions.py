from fastapi import HTTPException, status

class TokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

class GameFinished(Exception):
    def __init__(self, message="Game is already finished") -> None:
        self.message = message
        super().__init__(self.message)