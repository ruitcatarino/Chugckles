from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from utils.schemas import UserSchema
from utils.token import generate_token, jwt_required
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/user",
    tags=["Authentication"],
)


@router.post("/register")
async def register(user_model: UserSchema):
    if await User.exists(username=user_model.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {user_model.username} already taken",
        )
    user = await User.create(username=user_model.username, password=user_model.password)
    return {"message": f"User {user.username} created"}


@router.post("/token")
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


@router.get("/test")
async def test(user: UserSchema = Depends(jwt_required)):
    return {"message": f"Logged {user.username}"}
