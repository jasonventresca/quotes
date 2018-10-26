#!/bin/bash
set -eu

# Can be installed via `crontab`, e.g.
#       0 14 * * * /home/ubuntu/quotes/zen/send_all.sh

# Make sure we have everything necessary to run python 3 + pipenv. Cron does not have the same PATH by default as ubuntu's bash shell.
export PATH=/home/ubuntu/dotfiles.jason_ventresca/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/Users/jasonventresca/Library/Python/3.7/bin:/home/ubuntu/.local/bin

# Here's where our pipenv project lives
cd $HOME/quotes/zen

# Run it!
pipenv run ./mailer.py \
    1 >> ./send_all.out.log \
    2 >> ./send_all.err.log
