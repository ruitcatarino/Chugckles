from tortoise.models import Model
from tortoise import fields


class Card(Model):
    id = fields.IntField(pk=True)
    challenge = fields.TextField()
    deck = fields.ForeignKeyField("models.Deck", related_name="cards")

    class Meta:
        table = "cards"
        unique_together = (("challenge", "deck"),)
