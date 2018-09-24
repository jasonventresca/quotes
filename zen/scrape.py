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

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.author == other.author
        )

    def __lt__(self, other):
        l_key = (self.text, self.author)
        r_key = (other.text, other.author)
        return l_key < r_key

    def __hash__(self):
        return hash(self.text + self.author)

    def __str__(self):
        return '{}\n\n - {}'.format(
            self.text,
            self.author
        )

    def __repr__(self):
        return self.text[:20]

    def json(self):
        return json.dumps(
            {
                'text': self.text,
                'author': self.author,
            },
            indent=4,
            sort_keys=True,
        )


def get_url(year, month, page):
    return 'https://www.dailyzen.com/quotes/archive/{year}/{month:02d}/P{page:02d}'.format(
        year=year,
        month=month,
        page=page,
    )


def soup_from_url(url):
    resp = requests.get(url)
    return BeautifulSoup(resp.text, 'html.parser')


def get_quotes(soup):
    quotes = [x.text.strip() for x in soup.find_all('blockquote')]
    authors = [x.text.strip() for x in soup.find_all('cite')]
    assert len(quotes) == len(authors)
    for (text, author) in zip(quotes, authors):
        q = Quote(text, author)
        yield q


def generate_urls(start=None, end=None):
    start = start or START
    end = end or END

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
        for page in range(1, PAGES + 1):
            yield get_url(
                year=dt.year,
                month=dt.month,
                page=page,
            )


def main(*args, **kwargs):
    url = get_url(*args, **kwargs)
    soup = soup_from_url(url)
    return get_quotes(soup)


if __name__ == '__main__':
    # Example page to scrape -> https://www.dailyzen.com/quotes/archive/2015/01/P20
    pprint(tuple(main(year=2015, month=1, page=20)))
    pprint(tuple(generate_urls())[:20])
