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
        ## Fly related things
        # elif key == "fly":
        #     ft = FlyTransformer(Fly())
        #     ft.transform( tsLog, tsClient, tsReq, key, value)
        #     query = Fly.select().where(Fly.number == int(value))
        #     if query.exists():
        #         warnings.warn(f"Fly number {value} already exists")
        #         fly = query.get()
        #         if self.experiment.fly is None:
        #             self.experiment.fly = fly
        #         elif isinstance(self.experiment.fly, Fly):
        #             self.experiment.fly.copy_from(fly)
        #     else:
        #         self.experiment.fly = Fly.create(number = int(value))
            


# elf.sex = fly.sex
#         self.birth_after = fly.birth_after
#         self.birth_before = fly.birth_before
#         self.strain = fly.strain
#         self.batch = fly.batch
#         self.day_start = fly.day_start
#         self.day_end = fly.day_end
#         self.incubator_since




    def get_keys(self):
        pass
        
    
    def save(self) -> None:
        # self.experiment.fly.save()
        # self.experiment.ball.save()
        self.experiment.fly = self.flytransformer.fly
        self.experiment.save()
