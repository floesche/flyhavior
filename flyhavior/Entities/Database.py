from peewee import Model, SqliteDatabase

from Entities.Experiment import Experiment


class Database:

   

    _allEntities = [Experiment]

    def createTables(self) -> None:
        self.db.create_tables(self._allEntities)

