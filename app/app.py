from tools.config_manager import config
from parser import Parser, DATE_FORMAT
from os import getenv, putenv
from os.path import join as path_join
from datetime import datetime
from tools.email_server import EmailServer
import logging

KEY_FROM_DATE = "FROM_DATE"


def run():
    start_time = datetime.now()
    parser = Parser(
        config['source'],
        output_format=config['format'],
        modes=config['modes'],
        create_date=start_time,
        from_date=config.load_last_run()
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
                server.send_email(
                    output,
                    subject=getenv("EMAIL_SUBJECT"),
                    _to=config["email"],
                    _type=config["format"]
                )
                server.close()
            except Exception as e:
                logging.error("Can't send email: %s" % e)

    logging.debug("Store last run tm: %s" % start_time.strftime(DATE_FORMAT))
    config.store_last_run(start_time)

    if config["output"]:
        logging.debug("Store output file. Path: %s" % config["output"])
        with open(config["output"], "w") as f:
            f.write(output)

    if config["history"]:
        path = path_join(config["history"], "%s.%s" % (start_time.strftime('%s'), config["format"]))
        logging.debug("Store file for history. Path: %s" % path)
        with open(path, "w") as f:
            f.write(output)


