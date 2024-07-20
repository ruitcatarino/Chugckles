import asyncio
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from models import User, UserPydantic
from utils.settings import settings


class TokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def generate_token(username: str):
    expiration = datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_validity)
    payload = {
        "username": username,
        "exp": expiration,
    }
    return await asyncio.to_thread(
        jwt.encode, payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


async def decode_token(token: str) -> dict:
    try:
        payload = await asyncio.to_thread(
            jwt.decode,
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except InvalidTokenError:
        raise TokenException()


def jwt_required():
    def wrapper(func):
        async def decorated(
            credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        ):
            token = credentials.credentials
            payload = await decode_token(token)

            username = payload.get("username")
            exp_timestamp = payload.get("exp")

            if not username or not exp_timestamp:
                raise TokenException()

            if datetime.now(timezone.utc) > exp_timestamp:
                raise TokenException()

            user = await User.get_or_none(username=username)
            if not user or user.disabled:
                raise TokenException()

            user_pydantic = await UserPydantic.from_tortoise_orm(user)
            return await func(user_pydantic)

        return decorated

    return wrapper
