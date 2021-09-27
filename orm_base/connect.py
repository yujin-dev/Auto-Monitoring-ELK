from orm_base.table import *


class Schema(object):

    engine = None

    def __init__(self, name):
        self.name = name

    def __setattr__(self, key, value):
        if isinstance(value, TableBase):
            value.connect(self.engine)
        super().__setattr__(key, value)

    @classmethod
    def connect(cls, engine):
        cls.engine = engine
