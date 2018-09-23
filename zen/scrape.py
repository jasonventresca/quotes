#!/usr/bin/env python3

import json
from dateutil import rrule
from datetime import date, datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup


START = date(2015, 1, 1)
END = date(2018, 9, 1)
PAGES = 31 # TODO: Do we need to go all the way up to 31? Can we skip ahead every 4? (e.g. 1, 5, 9)


class Quote(object):
    def __init__(self, text, author=None):
        self.text = text
        self.author = author

    def __hash__(self):
        return hash(self.text + self.author)

    def __str__(self):
        return '{}\n\n - {}'.format(
            self.text,
            self.author
        )

    def __repr__(self):
        return '{}... - {}'.format(
            self.text[:40],
            self.author,
        )

    def json(self):
        return json.dumps({
            'text': self.text,
            'author': self.author,
        })


def get_url(year, month, page):
    month = str(month) if month > 9 else '0{}'.format(month) # TODO: is this necessary?
    return 'https://www.dailyzen.com/quotes/archive/{year}/{month}/P{page}'.format(
        year=year,
        month=month,
        page=page,
    )


def soup_from_url(url):
    resp = requests.get(url)
    return BeautifulSoup(resp.text, 'html.parser')


def get_quotes(soup):
    quotes = [x.text.strip() for x in soup.find_all('blockquote')]
    by = [x.text.strip() for x in soup.find_all('cite')]
    assert len(quotes) == len(by)
    for (text, author) in zip(quotes, by):
        q = Quote(text, author)
        yield q


def generate_urls(start=None, end=None):
    start = start or START
    end = end or END

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
        for page in range(1, PAGES + 1):
            yield "{year}/{month:02d}/{page:02d}".format(
                year=dt.year,
                month=dt.month,
                page=page,
            )


def main(*args, **kwargs):
    # 2015/01/P20
    url = get_url(*args, **kwargs)
    soup = soup_from_url(url)
    return get_quotes(soup)


if __name__ == '__main__':
    pprint(tuple(main(year=2015, month=1, page=20)))
    pprint(tuple(generate_urls())[:20])
