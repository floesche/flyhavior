from peewee import *

from Entities.BaseModel import BaseModel

from Entities.Condition import Condition
from Entities.Fictrac import Fictrac

class Rotation(BaseModel):

    condition = ForeignKeyField(Condition, null=True, backref='condition', on_update="CASCADE", on_delete="CASCADE")

    client_ts_ms = IntegerField(null=True)

    fictrac_seq = IntegerField(null=True, index=True)

    fictrac = ForeignKeyField(Fictrac, null=True, backref='fictrac', on_update='CASCADE', on_delete="CASCADE")

    rendered = BooleanField(default=False)

    speed = FloatField(null=True)
    angle = FloatField(null=True)
