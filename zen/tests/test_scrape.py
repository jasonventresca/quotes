#!/usr/bin/env python3

import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '..'))

from scrape import *


def test_quote_extractions():
    for i, quote in enumerate(get_quotes(year=2015, month=1, page=20)):
        fname = join(
            dirname(__file__),
            'data/{}.json'.format(i)
        )
        with open(fname, 'r') as f:
            expected = f.read()

        observed = quote.json()
        assert expected == observed


if __name__ == '__main__':
    test_quote_extractions()
