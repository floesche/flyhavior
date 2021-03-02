import warnings

from dateutil.parser import parse

from Entities.Fly import Fly

from Transformer.Transformer import Transformer



class FlyTransformer(Transformer):


    def __init__(self, fly) -> None:
        self.fly = fly
        self.switcher = {
            "fly" : self._flynumber,
            "sex" : self._sex,
            "birth-start" : self._birth_after,
            "birth-end" : self._birth_before,
    
            "fly-strain" : self._strain,
            "fly-batch" : self._batch,
            "day-start" : self._day_start,
            "day-end" : self._day_end,
            "day-night-since": self._incubator_since
        }

    def transform(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.switcher.get(key, self._nothingtosee)(tsLog, tsClient, tsReq, key, value)

    def _flynumber(self, tsLog, tsClient, tsReq, key, value):
        fly, created = Fly.get_or_create(number=int(value))
        fly.values_from(self.fly)
        self.fly = fly


    def _sex(self, tsLog, tsClient, tsReq, key, value):
        self.fly.sex = value.upper()

    def _birth_after(self, tsLog, tsClient, tsReq, key, value):
        self.fly.birth_after = parse(value)

    def _birth_before(self, tsLog, tsClient, tsReq, key, value):
        self.fly.birth_before = parse(value)

    def _strain(self, tsLog, tsClient, tsReq, key, value):
        self.fly.strain = value

    def _batch(self, tsLog, tsClient, tsReq, key, value):
        self.fly.batch = value

    def _day_start(self, tsLog, tsClient, tsReq, key, value):
        self.fly.day_start = parse(value).time()

    def _day_end(self, tsLog, tsClient, tsReq, key, value):
        self.fly.day_end = parse(value).time()

    def _incubator_since(self, tsLog, tsClient, tsReq, key, value):
        self.fly.incubator_since = parse(value).date()


    def _nothingtosee(self,  tsLog, tsClient, tsReq, key, value):
        print(f"Unknown key {key}")

    def get_keys(self):
        return self.switcher.keys()

