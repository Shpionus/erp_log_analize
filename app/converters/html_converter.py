from converter import BaseConverter
import os

FILE_PATH = os.path.abspath(os.path.dirname(__file__))

class HTMLConverter(BaseConverter):

    env = None
    template = None

    def setup(self):
        from jinja2 import Environment, FileSystemLoader
        self.env = Environment(loader=FileSystemLoader(os.path.join(FILE_PATH, 'templates', 'html')))
        self.template = self.env.get_template('template.html')

    def format(self):
        return self.template.render(parser=self.parser)


