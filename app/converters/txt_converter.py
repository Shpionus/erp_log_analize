from converter import BaseConverter
import os

FILE_PATH = os.path.abspath(os.path.dirname(__file__))

class Converter(BaseConverter):

    env = None
    template = None

    def setup(self):
        from jinja2 import Environment, FileSystemLoader
        self.env = Environment(loader=FileSystemLoader(os.path.join(FILE_PATH, 'templates', 'txt')))
        self.template = self.env.get_template('template.txt')

    def format(self):
        return self.template.render(parser=self.parser)
