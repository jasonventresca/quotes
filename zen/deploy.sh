#!/bin/bash
set -eu

CONF_FILES='
    .secrets.json
    recipients.txt
    all_quotes.json
'

echo "copying files to remote host"
for f in $CONF_FILES ; do
    #echo "copying $f to remote host..."
    scp $f foodieland:~/quotes/zen/
done

echo
echo "done :)"
