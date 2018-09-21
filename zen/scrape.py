#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup


def main():
    html_doc = requests.get('https://www.dailyzen.com/quotes/archive/2015/01/P20')
    soup = BeautifulSoup(html_doc, 'html.parser')
    print(soup)


if __name__ == '__main__':
    main()
