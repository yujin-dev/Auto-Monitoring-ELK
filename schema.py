from util import TableManager


class Schema(object):

    engine = None

    def __init__(self, name):
        self.name = name

    def __setattr__(self, key, value):
        if isinstance(value, TableManager):
            value.connect(self.engine)
        super().__setattr__(key, value)