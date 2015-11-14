from tools.config_manager import config
from parser import Parser


def run():

    parser = Parser(
        config['source'],
        output_format=config['format'],
        modes=config['modes']
    )
    parser.parse()
    output = parser.format()

    with open(config['output'], "w") as f:
        f.write(output)
