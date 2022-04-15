from peewee import *

from Entities.BaseModel import BaseModel

from Entities.Experiment import Experiment

class Condition(BaseModel):

    experiment = ForeignKeyField(Experiment, null=True, backref="experiment", on_update="CASCADE", on_delete="CASCADE")

    trial_number = IntegerField(null=True)
    trial_type = TextField(null=True, constraints=[Check('trial_type IN ("OPEN", "CLOSED")')])

    condition_number = IntegerField(null=True)
    condition_type = TextField(null=True, constraints=[Check('condition_type IN ("PRE", "POST", "OPEN", "CLOSED")')])

    fps = FloatField(null=True)
    bar_size = FloatField(null=True)
    interval_size = FloatField(null=True)

    comment = TextField(null=True)
    repetition = IntegerField(null=True)

    gain = FloatField(null=True)
    stimulus_type = TextField(null=True)
    start_orientation = FloatField(null=True)
