#!/bin/bash
set -eu

# Can be installed via `crontab`, e.g.
#       0 14 * * * /home/ubuntu/quotes/zen/send_all.sh

# Make sure we have everything necessary to run python 3 + pipenv. Cron does not have the same PATH by default as ubuntu's bash shell.
export PATH="$PATH":/home/ubuntu/.local/bin

# Here's where our pipenv project lives
cd $HOME/quotes/zen

# Run it!
pipenv run ./mailer.py >>./send_all.log 2>&1
