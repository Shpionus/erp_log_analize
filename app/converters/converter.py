import abc

class BaseConverter(object):
    __metaclass__ = abc.ABCMeta

    parser = None

    def __init__(self, parser):
        self.parser = parser
        self.setup()

    def setup(self):
        pass

    @abc.abstractmethod
    def format(self):
        pass
