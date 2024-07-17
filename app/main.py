from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from database import TORTOISE_ORM, init_db
from contextlib import asynccontextmanager
from routers import user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)
