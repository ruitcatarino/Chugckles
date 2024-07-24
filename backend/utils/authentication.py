import asyncio
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from models.user import User
from settings import settings
from utils.schemas import UserSchema
from utils.exceptions import TokenException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


async def generate_token(username: str) -> str:
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
        raise TokenException


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
