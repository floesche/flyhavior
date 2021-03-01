_all_tables = [Victim, Command, Topic, Message, Scan]


def create_db_connection():
    """ Creates a database connection with the postgres db"""

    is_test_env = os.getenv('MQTT_PWN_TESTING_ENV')

    if is_test_env:
        db = SqliteDatabase(':memory:')
    else:
        db = SqliteDatabase('data/test.db', pragmas={
            'journal_mode': 'wal',
            'cache_size': -1 * 64000,  # 64MB
            'foreign_keys': 1,
            'ignore_check_constraints': 0,
            'synchronous': 0})

    database_proxy.initialize(db)

    return db


def create_tables(db, tables):
    """ Creates the given tables """

    try:
        db.create_tables(tables)
    except ProgrammingError:
        pass


def create_all_tables(db):
    """ Creates all the tables """

    create_tables(db, _all_tables)


def truncate_all_tables(db):
    """ Truncates all database tables """

    db.drop_tables(_all_tables)
    create_tables(db, _all_tables)