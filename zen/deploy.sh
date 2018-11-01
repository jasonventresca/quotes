#!/bin/bash
set -eu

CONF_FILES='
    .secrets.json
    .gdrive_creds.json
    debug-recipients.txt
    all_quotes.json
'

echo "pulling the latest source code, and installing any required dependencies"
ssh -o PermitLocalCommand=no foodieland '
    cd ~/quotes/zen &&
    git pull origin master &&
    PATH="$PATH":"/home/ubuntu/.local/bin" pipenv install -r ./requirements.txt
'

echo "copying files to remote host"
for f in $CONF_FILES ; do
    #echo "copying $f to remote host..."
    scp $f foodieland:~/quotes/zen/
done

echo
echo "done :)"
