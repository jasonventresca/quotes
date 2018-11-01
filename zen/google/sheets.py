import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet(object):
    ''' Use a GoogleSheet object to establish a conenction with the Google Sheets API,
        and open a handle to a worksheet within a book (spreadsheet).
        You can then use .worksheet or .book to access methods/attributes of those
        underlying gspread objects.
    '''
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
            creds_filename,
            scope
        )

    '''
    def get_all_records(self):
        #return self.call_worksheet('get_all_records')
        return self.worksheet.get_all_records()

    def call_worksheet(self, func, *args, **kwargs):
        return getattr(self.worksheet, func)(*args, **kwargs)

    def call_book(self, func, *args, **kwargs):
        return getattr(self.book, func)(*args, **kwargs)
    '''
