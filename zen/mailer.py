#!/usr/bin/env python3

import os
import json
from datetime import datetime

import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail


CONFIG = None
START_DATE = datetime(2018, 10, 2)
NOW = datetime.now()


def main(msg_body, to_addr, from_addr=None):
    from_addr = from_addr or CONFIG.get('FROM_ADDRESS')
    sg = sendgrid.SendGridAPIClient(apikey=CONFIG.get('SENDGRID_API_KEY'))
    from_email = Email(from_addr)
    to_email = Email(to_addr)
    subject = "~ zen quote @ {} ~".format(NOW.strftime('%Y-%m-%d'))
    content = Content("text/plain", msg_body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == '__main__':
    # TODO: Install this repo and data files + secrets on ec2 box.
    with open('.secrets.json') as secrets_f:
        CONFIG = json.load(secrets_f)

    # TODO: Pull recipients from Google Sheets/Forms.
    # TODO: Create Google Form/Spreadsheet.
    with open('recipients.txt') as recip_f:
        recipients = tuple(x.strip() for x in recip_f)

    ## debug mode
    #recipients = ('jasonventresca@gmail.com',)

    with open('all_quotes.json') as quotes_f:
        quotes = json.load(quotes_f)

    num_quotes = len(quotes)

    days_elapsed = (NOW - START_DATE).days
    idx = days_elapsed % num_quotes
    chosen_quote = quotes[idx]
    msg_body = '{quote}\n\n{author}'.format(
        quote=chosen_quote['text'],
        author=chosen_quote['author'],
    )
    print("DEBUG: msg_body = {}".format(msg_body))

    for i, recip in enumerate(recipients):
        print('{:3d} sending quote to: {}'.format(i+1, recip))
        main(msg_body=msg_body, to_addr=recip)
