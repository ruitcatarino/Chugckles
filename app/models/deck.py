from tortoise.models import Model
from tortoise import fields
from models.card import Card


class Deck(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    cards: fields.ReverseRelation["Card"]

    class Meta:
        table = "decks"

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return str(self)
