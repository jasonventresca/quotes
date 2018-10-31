#!/usr/bin/env python

from os.path import join, dirname
from pprint import pprint

from sheets import GoogleSheet


def test_get_all_records():
    gs = GoogleSheet(
        book='zen_quotes',
        worksheet='subscribers',
        creds_filename=join(dirname(__file__), '..', '.gdrive_creds.json'),
    )

    pprint(gs.worksheet.get_all_records())


if __name__ == '__main__':
    test_get_all_records()
