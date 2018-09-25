#!/usr/bin/env python3

import sys
from os.path import join, dirname
import json
from collections import Counter
from pprint import pprint, pformat

sys.path.append(join(dirname(__file__), '..'))
import scrape


# TODO: Do a similar test, where right before diff'ing observed vs. expected,
#       we append a 'BROKEN' string onto observed, and assertRaises.
def test_quote_extractions():
    # TODO: Don't curl the website, instead pull from the checked in HTML file!
    for i, quote in enumerate(scrape.main(year=2015, month=1, page=20)):
        fname = join(
            dirname(__file__),
            'data/{}.json'.format(i)
        )
        with open(fname, 'r') as f:
            expected = f.read()

        observed = quote.json()
        assert expected == observed


def test_dedup_quotes_across_adjacent_pages():
    cross_page_quotes = []
    cross_page_quotes += list(scrape.main(year=2018, month=1, page=1))
    cross_page_quotes += list(scrape.main(year=2018, month=1, page=2))

    quotes_counter = Counter()
    for quote in cross_page_quotes:
        quotes_counter[quote] += 1
        #print('{}  -- hashes to -- {}'.format(
        #    repr(quote)[:10],
        #    hash(quote)
        #))

    fname = join(
        dirname(__file__),
        'data/dedup_quotes_across_adjacent_pages.pprint'
    )

    with open(fname, 'r') as f:
        expected = f.read()

    observed = pformat(quotes_counter, indent=4)
    assert expected == observed
