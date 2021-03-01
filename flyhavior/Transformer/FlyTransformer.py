import warnings

from Entities.Fly import Fly

from Transformer.Transformer import Transformer



class FlyTransformer(Transformer):


    def __init__(self, fly) -> None:
        self.fly = fly
        self.switcher = {
            "fly" : self._flynumber
        }

    def transform(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.switcher.get(key, self._nothingtosee)(tsLog, tsClient, tsReq, key, value)

    def _flynumber(self, tsLog, tsClient, tsReq, key, value):
        query = Fly.select().where(Fly.number == int(value))
        if query.exists():
            warnings.warn(f"Fly number {value} already exists")
            fly = query.get()
            if self.fly is None:
                self.fly = fly
            elif isinstance(self.fly, Fly):
                self.fly.copy_from(fly)
        else:
            self.experiment.fly = Fly.create(number = int(value))



    def _nothingtosee(self,  tsLog, tsClient, tsReq, key, value):
        print("Nothing to see")
        pass

    def get_keys(self):
        return self.switcher.keys()
