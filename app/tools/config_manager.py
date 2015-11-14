import optparse
import os
import datetime
import logging

from config import BASE_DIR


class ConfigManager(object):

    def __init__(self):

        self.options = {}
        self.parser = parser = optparse.OptionParser()

        # Server startup config
        group = optparse.OptionGroup(parser, "Common options")
        group.add_option(
            "-s", "--source",
            dest="source",
            help="Files for analise",
            default=False
        )
        group.add_option(
            "-o", "--output",
            dest="output",
            help="Result file",
            default=os.path.join(
                BASE_DIR,
                'output',
                'result_{salt}'.format(salt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
        )
        group.add_option(
            "-f", "--format",
            dest="format",
            help="Result's format",
            default="html"
        )

        group.add_option(
            "-t", "--types",
            dest="modes",
            help="Type of messages",
            default="ERROR,WARNING"
        )

        parser.add_option_group(group)

        for group in parser.option_groups:
            for option in group.option_list:
                self.options[option.dest] = option.default

        logging.basicConfig(
            format = u'%(asctime)s %(levelname)s ? %(filename)s #%(lineno)d - -  %(message)s',
            filename=os.path.join(BASE_DIR, "logs", "analyse.log"),
            level=logging.DEBUG
        )

    def parse_config(self, args=None):
        opt, args = self.parser.parse_args(args)

        keys = [
            "source", "output", "format", "modes"
        ]

        for arg in keys:
            if getattr(opt, arg):
                self.options[arg] = getattr(opt, arg)
            elif isinstance(self.options[arg], basestring) and self.casts[arg].type in optparse.Option.TYPE_CHECKER:
                self.options[arg] = optparse.Option.TYPE_CHECKER[self.casts[arg].type](self.casts[arg], arg, self.options[arg])

    def get(self, key, default=None):
        return self.options.get(key, default)

    def get_misc(self, sect, key, default=None):
        return self.misc.get(sect,{}).get(key, default)

    def __setitem__(self, key, value):
        self.options[key] = value

    def __getitem__(self, key):
        return self.options[key]

config = ConfigManager()
config.parse_config()