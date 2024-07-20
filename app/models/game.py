from tortoise.models import Model
from tortoise import fields


class Game(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField('models.User', related_name='games')

    class Meta:
        table = "games"

    def __str__(self):
        return self.name
    
