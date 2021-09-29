from _table import TableManager
from sqlalchemy import create_engine


class Schema(object):

    engine = None

    def __init__(self, name):
        self.name = name

    def __setattr__(self, key, value):
        if isinstance(value, TableManager):
            value.connect(self.engine)
        super().__setattr__(key, value)

    @classmethod
    def connect(cls, db_address):
        cls.engine = create_engine(db_address)
