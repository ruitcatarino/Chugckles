from utils.database import init_db
from models import *
import asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(init_db())


def arun(coro):
    return loop.run_until_complete(coro)
