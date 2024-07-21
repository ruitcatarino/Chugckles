from tortoise import Tortoise
from settings import settings
from models import Deck, Card
from utils import POPULATE_DATA

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    await prepopulate_db()


async def close_db():
    await Tortoise.close_connections()


async def prepopulate_db():
    if await Deck.all().count() == 0 and await Card.all().count() == 0:
        for deck_name, cards in POPULATE_DATA.items():
            new_deck = await Deck.create(name=deck_name)
            for card_data in cards:
                await Card.create(challenge=card_data, deck=new_deck)
