from peewee import *

from Entities.BaseModel import BaseModel

from Entities.Ball import Ball
from Entities.Fly import Fly


class Experiment(BaseModel):

    temperature = FloatField(null=True)
    air = TextField(null=True)
    glue = TextField(null=True)
    distance = FloatField(null=True)
    display = TextField(null=True)
    display_brightness = FloatField(null=True)
    display_color = TextField(null=True)

    ball = ForeignKeyField(Ball, null=True, backref='ball', on_update="CASCADE", on_delete="CASCADE")
    fly = ForeignKeyField(Fly, null=True, backref='fly', on_update="CASCADE", on_delete="CASCADE")

    starvation_start = DateTimeField(null=True)
    tether_start = DateTimeField(null=True)
    tether_end = DateTimeField(null=True)

