from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers import user
from tortoise.contrib.fastapi import register_tortoise
from utils.database import TORTOISE_ORM, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)

favicon_path = "favicon.ico"


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)
