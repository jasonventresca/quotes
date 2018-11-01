#!/bin/bash
set -eu

# TODO: Add Google Signed Credentials JSON file to this list.
CONF_FILES='
    .secrets.json
    .gdrive_creds.json
    debug-recipients.txt
    all_quotes.json
'

# TODO: ssh to foodieland, git pull the quotes repo, and pipenv install the requirements.txt
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
