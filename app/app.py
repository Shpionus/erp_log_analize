from tools.config_manager import config
from parser import Parser
from os import getenv
from os.path import join as path_join
from datetime import datetime
from tools.email_server import EmailServer
import logging


def run():

    start_time = datetime.now()

    parser = Parser(
        config['source'],
        output_format=config['format'],
        modes=config['modes']
    )

    parser.parse()
    output = parser.format()

    if config["email"]:
        if parser.data or not config["skip_empty"] :
            try: 
                server = EmailServer(
                    getenv("SMTP_SERVER"),
                    getenv("SMTP_PORT"),
                    getenv("SMTP_USER"),
                    getenv("SMTP_PASSWORD"),
                    getenv("SMTP_TLS", "false").lower() in ["true", "1", "y"],
                )
                server.send_email(output, getenv("EMAIL_SUBJECT"), getenv("EMAIL_SENDER"), config["email"], config["format"])
                server.close()
            except Exception as e:
                logging.error("Can't send email: %s" % e)
        
    if config["output"]:
        logging.debug("Store output file. Path: %s" % config["output"])
        with open(config["output"], "w") as f:
            f.write(output)

    if config["history"]:
        path = path_join(config["history"], "%s.%s" % (start_time.strftime('%s'), config["format"]))
        logging.debug("Store file for history. Path: %s" % path)
        with open(path, "w") as f:
            f.write(output)

            
