from fastapi import APIRouter, HTTPException, status
from models.user import User, UserPydantic
from utils.token import generate_token, jwt_required

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/register")
async def register(user_model: UserPydantic):
    if await User.exists(username=user_model.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {user_model.username} already taken",
        )
    user = await User.create(username=user_model.username, password=user_model.password)
    return {"message": f"User {user.username} created"}


@router.get("/login")
async def login(user_model: UserPydantic):
    user = await User.filter(username=user_model.username).first()
    if user is None or not await user.check_password(user_model.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error on Login"
        )
    return {
        "message": f"Logged in as {user.username}",
        "token": await generate_token(username=user.username),
    }


@router.get("/test")
@jwt_required()
async def test(user: UserPydantic):
    return {"message": f"Logged {user.username}"}
