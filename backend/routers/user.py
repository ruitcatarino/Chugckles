from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from utils.authentication import generate_token
from utils.schemas import UserSchema
from settings import settings

router = APIRouter(
    prefix="/user",
    tags=["Authentication"],
)


@router.post("/register")
async def register(user_model: UserSchema):
    if settings.allow_registrations is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registrations are not allowed at this time.",
        )
    
    if await User.exists(username=user_model.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {user_model.username} already taken",
        )
    user = await User.create(username=user_model.username, password=user_model.password)
    return {"message": f"User {user.username} created"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if user is None or not await user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error on Login"
        )
    return {
        "message": f"Logged in as {user.username}",
        "token": await generate_token(username=user.username),
    }
