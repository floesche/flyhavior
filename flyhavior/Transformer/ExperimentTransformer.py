import warnings

from datetime import timezone, timedelta, datetime

from dateutil.parser import parse

from Entities.Experiment import Experiment
from Entities.Ball import Ball
from Entities.Fly import Fly

from Transformer.Transformer import Transformer
from Transformer.FlyTransformer import FlyTransformer
from Transformer.ConditionTransformer import ConditionTransformer

class ExperimentTransformer(Transformer):

    def __init__(self, experiment) -> None:
        self.transformer = list()
        self.experiment = experiment
        self.experiment.save()
        self.experiment.fly = Fly()
        self._client_base_time = []
        #self.flytransformer = FlyTransformer(self.experiment.fly)
        self.flytransformer = FlyTransformer(self.experiment.fly)
        self.conditiontransformer = ConditionTransformer(self.experiment)

        self.switcher = {
            "de-start-experiment": self._start_time,
            "temperature" : self._temperature,
            "air" : self._air,
            "glue": self._glue,
            "distance": self._distance,
            "display": self._display,
            "screen-brightness": self._screen_brightness,
            "color": self._display_color,
            "starvation-start": self._starvation_start,
            "tether-start": self._tether_start,
            "tether-end": self._tether_stop,
            "protocol": self._protocol,
            "ball": self._ball,
            "block-repetition": self._time_sync
        }



    def addTransformer(self, transformer) -> None:
        self.transformer.append(transformer)

    def transform(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.switcher.get(key, self._other_transforms)(tsLog, tsClient, tsReq, key, value)
        if key in self.flytransformer.get_keys():
            self.flytransformer.transform(tsLog, tsClient, tsReq, key, value)
        if key in self.conditiontransformer.get_keys():
            self.conditiontransformer.transform(tsLog, tsClient, tsReq, key, value)
        else:
            # print(f"Unknown key {key}")
            pass


    def _other_transforms(self,  tsLog, tsClient, tsReq, key, value):
        self.experiment.end = datetime.fromtimestamp(float(tsLog) / 1000000000, timezone(timedelta(hours=-5)))

    def _start_time(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.start = datetime.fromtimestamp(float(tsLog) / 1000000000, timezone(timedelta(hours=-5)))

    def _temperature(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.temperature = float(value)

    def _air(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.air = value

    def _glue(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.glue = value

    def _distance(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.distance = float(value)

    def _display(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.display = value

    def _screen_brightness(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.display_brightness = float(value)/100

    def _display_color(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.display_color = value

    def _starvation_start(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.starvation_start = parse(value)

    def _tether_start(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.tether_start = parse(value)

    def _tether_stop(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.tether_end = parse(value)

    def _protocol(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.protocol = value

    def _ball(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.experiment.ball, created = Ball.get_or_create(number=int(value))
    
    def _time_sync(self, tsLog, tsClient, tsReq, key, value) -> None:
        self._client_base_time.append(int(tsReq) - float(tsClient) * 1000000)
        self.experiment._client_start = datetime.fromtimestamp((sum(self._client_base_time)/len(self._client_base_time))/ 1000000000, timezone(timedelta(hours=-5)))


    def get_keys(self):
        return self.switcher.keys()

    def save(self) -> None:
        self.experiment.fly = self.flytransformer.fly
        self.experiment.fly.save()
        self.experiment.save()
