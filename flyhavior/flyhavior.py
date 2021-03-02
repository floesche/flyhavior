"""Main module."""

import csv

from Transformer.ExperimentTransformer import ExperimentTransformer
# from Transformer.FlyFlixFile import FlyFlixFile

# from Entities.Database import Database

from Entities.BaseModel import db
from Entities.Experiment import Experiment
from Entities.Ball import Ball
from Entities.Fly import Fly
from Entities.Condition import Condition

class Flyhavior:

    def __init__(self, fnFlyFlix, fnFicTrac, fnDB) -> None:
        db.create_tables([Experiment, Ball, Fly, Condition])
        self.fnFlyFlix = fnFlyFlix
        self.fnFicTrac = fnFicTrac
        self.fnDB = fnDB
        self.experiment = Experiment()
        self.transformer = ExperimentTransformer(self.experiment)

    def run(self) -> None:

        # Database.createTables()
        with open(self.fnFlyFlix) as fffile:
            ffreader = csv.DictReader(fffile, fieldnames = ["ts", "tsClient", "tsReq", "key", "value"])
            for row in ffreader:
                self.transformer.transform(row["ts"], row["tsClient"], row["tsReq"], row["key"], row["value"])
        
        self.transformer.save()

        print(f"Generated experiment with id {self.experiment.id}")
