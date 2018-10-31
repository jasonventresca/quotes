#!/usr/bin/env python

print('testing gdrive')

print(
'''
TODO:
    √ pipenv add gdrive (also add to requirements.txt)
        √ also oauth2client + PyOpenSSL
    √ load Signed Credentials from .gdrive_creds.json
    √ adapt example from https://gspread.readthedocs.io/en/latest/oauth2.html
    - backup the credentials file! (Dropbox?)
'''
)

from os.path import join, dirname
from pprint import pprint

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SheetReader(object):
    def __init__(self, book, worksheet, creds_filename):
        ''' :param creds_filename: Credentials filename should be a JSON file for a Service Account.
                                   See https://gspread.readthedocs.io/en/latest/oauth2.html#using-signed-credentials
        '''
        self._creds = self._read_creds(creds_filename)
        self._gc = gspread.authorize(self._creds)
        self.book = self._gc.open(book)
        self.worksheet = self.book.worksheet(worksheet)

    @staticmethod
    def _read_creds(creds_filename):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        return ServiceAccountCredentials.from_json_keyfile_name(
            join(dirname(__file__), creds_filename),
            scope
        )

    def get_all_records(self):
        return self.worksheet.get_all_records()


def main():
    sheet_reader = SheetReader(
        book='zen_quotes',
        worksheet='subscribers',
        creds_filename='.gdrive_creds.json',
    )

    pprint(sheet_reader.get_all_records())


if __name__ == '__main__':
    main()
