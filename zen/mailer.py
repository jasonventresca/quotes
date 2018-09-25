#!/usr/bin/env python3

from flask import Flask
from flask_mail import Mail, Message
import os

CREDS = {}

def main():
    app = Flask(__name__)

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": CREDS['gmail username'],
        "MAIL_PASSWORD": CREDS['gmail password']
    }

    app.config.update(mail_settings)
    mail = Mail(app)


if __name__ == '__main__':
    with open('.secrets.json') as secrets_f:
        CREDS = json.load(secrets_f)

    main()
