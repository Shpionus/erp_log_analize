erp_log_analyzer
=================

A little script which allows retrive most important information from logs in convinient way.

Setup
-----

Clone the project and run setup script

```bash
./setup.sh
```

Then update `.env` file.
It contains following settings:
```
# Email server
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="***"
SMTP_PASSWORD="***"
SMTP_ENCODING=ssl or tls

# Email message
EMAIL_SUBJECT="Odoo server logs report (test from local machine)"
```

Usage
-----

There are many different parameters. You can check them all with following command:
```bash
$ python run.py -h
```
```
Usage: run.py [options]

Options:
  -h, --help            show this help message and exit

  Common options:
    -s SOURCE, --source=SOURCE
                        Files for analise
    -o OUTPUT, --output=OUTPUT
                        Result file
    -f FORMAT, --format=FORMAT
                        Result's format
    -t MODES, --types=MODES
                        Type of messages
    -e ENV, --env=ENV   .env file
    --history=HISTORY   Directory to store history

  Email options:
    --email=EMAIL       Send email with report to this address(es)
    --skip-empty=SKIP_EMPTY
                        Do not send email if not fund target messages
```

F.ex.
-----

Check errors and wornings (default mode) in `/var/logs/odoo/server.log` and prepare report in html format:
```bash
python run.py --source /var/logs/odoo/server.log -f html
```

Check errors only end send email with plain text report:
```bash
python run.py --source /var/logs/odoo/server.log -t error -f txt --email your_email@domain.com
```

The same, but do not send email if no errors found:
```bash
python run.py --source /var/logs/odoo/server.log -t error -f txt --email your_email@domain.com --skip-empty true
```

Prepare report and store it in `~/report.html` and do not store history:
```bash
python run.py --source /var/logs/odoo/server.log -f html -o ~/report.html --history false
```
