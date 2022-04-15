"""Main module."""

import csv

from Transformer.ExperimentTransformer import ExperimentTransformer
from Transformer.FictracTransformer import FictracTransformer
# from Transformer.FlyFlixFile import FlyFlixFile

# from Entities.Database import Database

from Entities.BaseModel import db
from Entities.Experiment import Experiment
from Entities.Ball import Ball
from Entities.Fly import Fly
from Entities.Condition import Condition
from Entities.Rotation import Rotation
from Entities.Fictrac import Fictrac


class Flyhavior:

    def __init__(self, fnFlyFlix, fnFicTrac, fnDB) -> None:
        db.create_tables([Experiment, Ball, Fly, Condition, Rotation, Fictrac])
        self.fnFlyFlix = fnFlyFlix
        self.fnFicTrac = fnFicTrac
        self.fnDB = fnDB
        self.experiment = Experiment()
        self.transformer = ExperimentTransformer(self.experiment)

    def run(self) -> None:

        # Database.createTables()
        with open(self.fnFlyFlix) as fffile:
            ffreader = csv.DictReader(fffile, fieldnames=["ts", "tsClient", "tsReq", "key", "value"])
            for row in ffreader:
                #if row["tsClient"] != "clientTS" and int(row["tsClient"]) < 5990098: ### Hack for data on 2022
                self.transformer.transform(row["ts"], row["tsClient"], row["tsReq"], row["key"], row["value"])

        self.transformer.save()

        fictracTransformer = FictracTransformer(self.fnFicTrac, self.experiment)
        fictracTransformer.run()

        print(f"Generated experiment with id {self.experiment.id}")
