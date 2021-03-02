from peewee import IntegerField, FloatField

from Entities.BaseModel import BaseModel

class Ball(BaseModel):

    number = IntegerField(unique=True)
    weight = FloatField(null=True)
