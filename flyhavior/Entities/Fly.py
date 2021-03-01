from peewee import *

from Entities.BaseModel import BaseModel

class Fly(BaseModel):

    number = IntegerField(primary_key=True)
    sex = TextField(null=True, constraints=[Check('sex IN ("F", "M")')])
    birth_after = DateTimeField(null=True)
    birth_before = DateTimeField(null=True)
    
    strain = TextField(null=True)
    batch = TextField(null=True)
    day_start = TimeField(null=True)
    day_end = TimeField(null=True)
    incubator_since = DateField(null=True)
    

    def values_from(self, fly) -> None:
        if fly.number is not None and self.number is None:
            self.number = fly.number
        else:
            warnings.warn(f"Conflict for fly number: source {fly.number} and target {self.number}")
        
        if fly.sex is not None and self.sex is None:
            self.sex = fly.sex
        else:
            warnings.warn(f"Conflict for fly number {fly.number}: source sex {fly.sex} and target {self.sex}")

        if fly.birth_after is not None and self.birth_after is None:
            self.birth_after = fly.birth_after
        else:
            warnings.warn(f"Conflict for fly number {fly.number}: source birth after {fly.birth_after} and target {self.birth_after}")

        if fly.birth_before is not None and self.birth_before is None:
            self.birth_before = fly.birth_before
        else:
            warnings.warn(f"Conflict for fly number {fly.number}: source birth before {fly.birth_before} and target {self.birth_before}")

        if fly.strain is not None and self.strain is None:
            self.strain = fly.strain
        else:
            warnings.warn(f"Conflict for fly number {fly.number}: source fly strain {fly.strain} and target {self.strain}")

        if fly.batch is not None and self.batch is None:
            self.batch = fly.batch
        else:
            warnings.warn(f"Conflict for fly number {fly.number}: source fly batch {fly.batch} and target {self.batch}")

        if fly.day_start is not None and self.day_start is None:
            self.day_start = fly.day_start
        else:
            warnings.warn(f"Conflict for fly number {fly.number}: source day starts at {fly.day_start} and target {self.day_start}")

        if fly.day_end is not None and self.day_end is None:
            self.day_end = fly.day_end
        else:
            warnings.warn(f"Conflict for fly number {fly.number}: source day ends at {fly.day_end} and target {self.day_end}")

        if fly.incubator_since is not None and self.incubator_since is None:
            self.incubator_since = fly.incubator_since
        else:
            warnings.warn(f"Conflict for fly number {fly.number}: source has been in the incubator since {fly.incubator_since} and target {self.incubator_since}")
