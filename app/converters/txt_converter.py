import os

from converter import BaseConverter


FILE_PATH = os.path.abspath(os.path.dirname(__file__))


class Converter(BaseConverter):

    env = None
    template = None

    def setup(self):
        from jinja2 import Environment, FileSystemLoader
        from app.converters.utils.jinja_filters import jinia_filters
        self.env = Environment(loader=FileSystemLoader(os.path.join(FILE_PATH, 'templates', 'txt')))
        self.env.filters.update(jinia_filters)
        self.template = self.env.get_template('template.txt')

    def format(self):
        return self.template.render(parser=self.parser)
