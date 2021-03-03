from peewee import *

from Entities.BaseModel import BaseModel

from Entities.Experiment import Experiment

class Fictrac(BaseModel): 
    
    frame_counter = IntegerField()

    experiment = ForeignKeyField(Experiment, null=True, backref='experiment', on_update="CASCADE", on_delete="CASCADE")

    d_cam_x = FloatField()
    d_cam_y = FloatField()
    d_cam_z = FloatField()
    err = FloatField()
    
    d_lab_x = FloatField()
    d_lab_y = FloatField()
    d_lab_z = FloatField()

    cam_x = FloatField()
    cam_y = FloatField()
    cam_z = FloatField()

    lab_x = FloatField()
    lab_y = FloatField()
    lab_z = FloatField()

    integrated_lab_x = FloatField()
    integrated_lab_y = FloatField()

    animal_lab_heading = FloatField()
    animal_lab_movement = FloatField()
    animal_speed = FloatField()

    integrated_movement_x = FloatField()
    integrated_movement_y = FloatField()

    timestamp = FloatField()

    seq = IntegerField(index=True)

    delta_timestamp = FloatField()

    alternative_timestamp = FloatField()


