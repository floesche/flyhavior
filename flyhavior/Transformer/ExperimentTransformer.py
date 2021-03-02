import warnings

from Entities.Experiment import Experiment
from Entities.Ball import Ball
from Entities.Fly import Fly

from Transformer.Transformer import Transformer
from Transformer.FlyTransformer import FlyTransformer

class ExperimentTransformer(Transformer):

    def __init__(self, experiment) -> None:
        self.transformer = list()
        self.experiment = experiment
        self.experiment.fly = Fly()
        #self.flytransformer = FlyTransformer(self.experiment.fly)
        self.flytransformer = FlyTransformer(self.experiment.fly)

    def addTransformer(self, transformer) -> None:
        self.transformer.append(transformer)

    def transform(self, tsLog, tsClient, tsReq, key, value) -> None:
        if key == "temperature":
            self.experiment.temperature = float(value)
        elif key == "air":
            self.experiment.air = value
        elif key == "glue":
            self.experiment.glue = value
        elif key == "distance":
            self.experiment.distance = float(value)
        elif key == "display":
            self.experiment.display = value
        elif key == "screen-brightness":
            self.experiment.display_brightness = float(value)
        elif key == "color":
            self.experiment.display_color = value
        elif key == "ball":
            query = Ball.select().where(Ball.number == int(value))
            if query.exists():
                self.experiment.ball = query.get()
            else:
                self.experiment.ball = Ball.create(number = int(value))
        elif key in self.flytransformer.get_keys():
            self.flytransformer.transform(tsLog, tsClient, tsReq, key, value)





    def get_keys(self):
        pass
        
    
    def save(self) -> None:
        self.experiment.fly = self.flytransformer.fly
        self.experiment.fly.save()
        self.experiment.save()
