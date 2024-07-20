from tortoise.models import Model
from tortoise import fields


class Card(Model):
    id = fields.IntField(pk=True)
    challenge = fields.TextField()
    deck = fields.ForeignKeyField("models.Deck", related_name="cards")

    class Meta:
        table = "cards"

    def __str__(self):
        return f"Card#{self.id}@{self.deck.name}: {self.challenge}"
    
    def __repr__(self):
        return str(self)
