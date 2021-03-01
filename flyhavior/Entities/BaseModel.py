from peewee import Model, SqliteDatabase

db = SqliteDatabase('data/test.db', pragmas={
        'journal_mode': 'wal',
        'cache_size': -1 * 64000,  # 64MB
        'foreign_keys': 1,
        'ignore_check_constraints': 0,
        'synchronous': 0})

class BaseModel(Model):

    class Meta:
        database = db