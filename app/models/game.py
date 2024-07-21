from tortoise.models import Model
from tortoise import fields


class Game(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    creator = fields.ForeignKeyField("models.User", related_name="games")
    decks = fields.ManyToManyField("models.Deck", related_name="decks")
    num_players = fields.IntField()
    players = fields.JSONField()
    state = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    finished = fields.BooleanField(default=False)

    class Meta:
        table = "games"

    def __str__(self):
        return self.name

    @property
    async def is_finished(self):
        return self.finished
