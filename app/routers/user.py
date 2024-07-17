from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import User

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


class UserModel(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user_model: UserModel):
    if await User.exists(username=user_model.username):
        raise HTTPException(
            status_code=406, detail=f"Username {user_model.username} already taken"
        )
    user = await User.create(username=user_model.username, password=user_model.password)
    return {"messages": f"User {user} created"}


@router.get("/login")
async def login(user_model: UserModel):
    user = await User.filter(username=user_model.username).first()
    if user is None or not user.check_password(user_model.password):
        raise HTTPException(status_code=406, detail=f"Error on Login")
    return {"messages": f"Logged in as {user}"}

