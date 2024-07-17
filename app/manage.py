from tortoise import run_async
from database import init_db


async def create_db_schemas():
    run_async(init_db())
