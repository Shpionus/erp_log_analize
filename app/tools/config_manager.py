import optparse
import os
import datetime
import logging
from dotenv import load


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
            default=None
        )
        group.add_option(
            "-o", "--output",
            dest="output",
            help="Result file",
            default=None
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
        group.add_option(
            "-e", "--env",
            dest="env",
            help=".env file",
            default=os.path.join(BASE_DIR, ".env")
        )
        group.add_option(
            "--history",
            dest="history",
            help="Directory to store history",
            default=os.path.join(BASE_DIR, "history")
        )
        parser.add_option_group(group)

        # Email setup
        email_group = optparse.OptionGroup(parser, "Email options")
        email_group.add_option(
            "--email",
            dest="email",
            help="Send email with report to this address(es)",
            default=None
        )
        email_group.add_option(
            "--skip-empty",
            dest="skip_empty",
            help="Do not send email if not fund target messages",
            default=False
        )
        parser.add_option_group(email_group)

        for group in parser.option_groups:
            for option in group.option_list:
                self.options[option.dest] = option.default

        logging.basicConfig(
            format=u'%(asctime)s %(levelname)s ? %(filename)s #%(lineno)d - -  %(message)s',
            filename=os.path.join(BASE_DIR, "logs", "analyse.log"),
            level=logging.DEBUG
        )

    def load_env(self):
        load(filepath=self.get("env"))

    def parse_config(self, args=None):
        (opt, args) = self.parser.parse_args(args)
        self.options = opt

    def get(self, key, default=None):
        return self.options.ensure_value(key, default)

    def __setitem__(self, key, value):
        setattr(self.options, key, value)

    def __getitem__(self, key):
        return self.get(key)


config = ConfigManager()
config.parse_config()
config.load_env()
