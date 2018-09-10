import glob
import os
import re
import logging
from datetime import datetime

from importlib import import_module


class UnsupportedFormat(Exception):
    pass


class Normalizer(object):

    group_patterns = [
        (re.compile(r'\(\s*\d*\s*\)'), '(xxx)'),
        (re.compile(r'=\d+(\.\d+)?'), '=xxx'),
        (re.compile(r'\b[a-z0-9\.\+_-]+@[a-z0-9\._-]+\.[a-z]*\b\s*', re.I), 'xxx@xxx.xxx '),
        (re.compile(r'\[\d{2}/[a-z]+/\d{4} \d{2}:\d{2}:\d{2}\]', re.I), '[XX/XX/XXXX XX:XX:XX] '),
    ]

    def group(self, group):
        if group:
            for regexp, val in self.group_patterns:
                group = regexp.sub(val, group)
        return group


class Parser(object):

    default_modes = [
        "warning",
        "error"
    ]

    Converter = None

    def __init__(self, source, output_format=None, modes=None):
        self.source = source
        self.source_files = []
        self.nm = Normalizer()

        if output_format is None:
            output_format = 'html'

        self.create_date = datetime.now()

        if modes:
            if isinstance(modes, (str, unicode)):
                modes = [x.strip().lower() for x in re.split('[\W]+', modes) if x.strip()]

        if not modes:
            modes = self.default_modes
        if 'error' in modes:
            modes.insert(0, modes.pop(modes.index('error')))

        self.modes = modes
        self.data = {
            "files": {},
            "messages": {x: {} for x in self.modes}
        }

        try:
            self.output_format = output_format
            module = import_module('app.converters.{format}_converter'.format(format=output_format))
            self.Converter = module.Converter

            if not self.Converter:
                raise UnsupportedFormat()

        except:
            raise Exception("Unavailable format specified")

    def parse(self):
        logging.info("Start parsing".format(source=self.source))

        self.prepare_list_of_files()
        for path in self.source_files:
            self.parse_file(path)

    def prepare_list_of_files(self):
        logging.info("Prepare list of files: {source}".format(source=self.source))
        if self.source:
            patterns = self.source.split(",")
            for pattern in patterns:
                if pattern:
                    abs_path = os.path.abspath(pattern)
                    for path in glob.glob(abs_path):
                        if os.path.isfile(path):
                            self.source_files.append(path)

        logging.info("List of files: {files}".format(files="; ".join(self.source_files)))

    def parse_file(self, path):
        logging.info("Parse file: {path}".format(path=path))
        self.data['files'][path] = {}

        pattern = re.compile(
            r"^(?P<str_date>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+(?P<code>\d+)\s+(?P<mode>\w+)\s+(?P<source>[\w\?]+)\s+(?P<logger>[^:]+):\s+(?P<group>.*)$",
            flags=re.I
        )
        groups = [
            'str_date',
            'code',
            'mode',
            'source',
            'group',
            'logger',
        ]

        count_of_lines = 0
        c_line = {}

        with open(path) as file_obj:
            for line in file_obj:
                count_of_lines += 1
                parts = re.match(pattern, line)
                if parts:

                    self.add_line(c_line)
                    c_line = {x: parts.group(x) for x in groups}
                    if c_line['mode']:
                        c_line['mode'] = c_line['mode'].lower()
                    if c_line['str_date']:
                        c_line['date'] = datetime.strptime(c_line['str_date'], '%Y-%m-%d %H:%M:%S,%f')

                else:
                    c_line['message'] = "".join([c_line.get('message') or '', line or ''])

        self.data['files'][path]['count_of_lines'] = count_of_lines

    def add_line(self, line_obj):
        if line_obj:
            if not line_obj.get("message"):
                line_obj["message"] = ""
            line_obj["base_group"] = self.nm.group(line_obj["group"])
            if line_obj.get('mode', None) in self.modes:
                mode = self.data['messages'][line_obj['mode']]

                base_group = mode.get(line_obj['base_group'])
                if not base_group:
                    base_group = mode[line_obj['base_group']] = {}

                message = base_group.get(line_obj['message'] or '')
                if message is None:
                    message = base_group[line_obj['message']] = {}

                logger = message.get(line_obj['logger'])
                if logger is None:
                    logger = message[line_obj['logger']] = {}

                group = logger.get(line_obj['group'])
                if group is None:
                    group = logger[line_obj['group']] = []

                group.append(line_obj['date'])

    def format(self):
        logging.info("Format to {format}".format(format=self.output_format))
        converter = self.Converter(self)
        return converter.format()
