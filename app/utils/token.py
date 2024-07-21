import asyncio
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from models.user import User
from utils.schemas import UserSchema
from utils.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def generate_token(username: str):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_validity)
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


async def jwt_required(token: str = Depends(oauth2_scheme)) -> UserSchema:
    payload = await decode_token(token)

    username = payload.get("username")
    exp_timestamp = payload.get("exp")

    if not username or not exp_timestamp:
        raise TokenException

    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

    if datetime.now(timezone.utc) > exp_datetime:
        raise TokenException

    user = await User.get_or_none(username=username)
    if user is None or user.disabled:
        raise TokenException

    return await UserSchema.from_tortoise_orm(user)
