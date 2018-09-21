#!/usr/bin/env python3

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), '..'))
from scrape import *


# TODO: Do a similar test, where right before diff'ing observed vs. expected,
#       we append a 'BROKEN' string onto observed, and assertRaises.
def test_quote_extractions():
    # TODO: Don't curl the website, instead pull from the checked in HTML file!
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
