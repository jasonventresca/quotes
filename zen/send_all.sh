#!/bin/bash
set -eu

# Can be installed via `crontab`, e.g.
#       0 14 * * * /home/ubuntu/quotes/zen/send_all.sh

(
    cd $HOME/quotes/zen
    pipenv run ./mailer.py
)
