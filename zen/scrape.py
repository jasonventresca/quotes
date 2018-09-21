#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup


def main():
    resp = requests.get('https://www.dailyzen.com/quotes/archive/2015/01/P20')
    soup = BeautifulSoup(resp.text, 'html.parser')
    quotes = soup.find_all('blockquote')
    by = soup.find_all('cite')
    assert len(quotes) == len(by)
    print('{}\n\n- by {}'.format(
        quotes[0], by[0]
    ))


if __name__ == '__main__':
    main()
