## How To
To run the scraper:

`pipenv run ./scrape.py`

## Notes
Next Steps
    - Make it easier to add more recipients
    - Recipients are currently stored in a JSON file, not version controlled.
    - Super easy thing to implement is to add JSON file to version control
        - Cannot push to public github, because I don't want to expose people's email addresses.
        - Could track the file in my Dropbox account.
    ~ A better idea is to track the recipients as a spreadsheet in Google Drive.
        - Use gspread or something to import the recipients into the Python mail-sending code.
        - Probably a good thing to sink effort into learning, could be broadly applicable for other projects!
    - Even fancier would be a Google Form that anyone can access to add themself.
        - Would need a way for me to remove people.
        - Can you edit the spreadsheet the form is dumping into?
