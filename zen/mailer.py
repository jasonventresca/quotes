#!/usr/bin/env python3

import os
import json
from datetime import datetime
from os.path import join, dirname
import argparse
import pprint

import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

from google.sheets import GoogleSheet


CONFIG = None
START_DATE = datetime(2018, 10, 2)
NOW = datetime.now()

DEBUG_RECIPIENTS_FILENAME = 'debug-recipients.txt'
USE_DEBUG_RECIPIENTS = False
NO_SEND = False


def get_subscribers():
    ''' Returns a list of dicts, where each list element is a person with Email + Name.
        For example: [{'Email': 'someone@website.com', 'Name': 'first-name'},]
    '''
    if USE_DEBUG_RECIPIENTS:
        with open(DEBUG_RECIPIENTS_FILENAME) as recip_f:
            email_name_pairs = [line.strip().split() for line in recip_f]
            debug_subscribers = [{'Email': email, 'Name': name} for (email, name) in email_name_pairs]

        return debug_subscribers

    gs = GoogleSheet(
        book='zen_quotes',
        worksheet='subscribers',
        creds_filename=join(dirname(__file__), '.gdrive_creds.json'),
    )

    return gs.worksheet.get_all_records()


def send_email(msg_body, to_addr, from_addr=None):
    if NO_SEND:
        return

    from_addr = from_addr or CONFIG.get('FROM_ADDRESS')
    sg = sendgrid.SendGridAPIClient(apikey=CONFIG.get('SENDGRID_API_KEY'))
    from_email = Email(from_addr)
    to_email = Email(to_addr)
    subject = "~ zen quote @ {} ~".format(NOW.strftime('%Y-%m-%d'))
    content = Content("text/plain", msg_body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    #logging.debug(response.status_code)
    #logging.debug(response.body)
    #logging.debug(response.headers)


def main():
    subscribers = get_subscribers()

    #logging.debug("subscribers:")
    #logging.debug(pprint.pformat(subscribers, indent=4))

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
    #logging.debug("msg_body = {}".format(msg_body))

    for i, subscr in enumerate(subscribers):
        if not subscr['Email']:
            print('{:3d} WARNING: skipping subscriber: {}'.format(i+1, subscr))
            continue

        print('{:3d} sending quote to: {}'.format(i+1, subscr))
        send_email(msg_body=msg_body, to_addr=subscr['Email'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--use-debug-recipients', action='store_true',
        help='Only send to folks in {}'.format(DEBUG_RECIPIENTS_FILENAME)
    )
    parser.add_argument(
        '-n', '--no-send', action='store_true',
        help='Do not actually send any emails. Print to screen only.'
    )
    args = parser.parse_args()

    USE_DEBUG_RECIPIENTS = args.use_debug_recipients
    NO_SEND = args.no_send

    # TODO: Install this repo and data files + secrets on ec2 box.
    with open('.secrets.json') as secrets_f:
        CONFIG = json.load(secrets_f)

    main()
