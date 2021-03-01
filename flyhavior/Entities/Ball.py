from peewee import IntegerField, FloatField

from Entities.BaseModel import BaseModel

class Ball(BaseModel):

    number = IntegerField(primary_key=True)
    weight = FloatField(null=True)
