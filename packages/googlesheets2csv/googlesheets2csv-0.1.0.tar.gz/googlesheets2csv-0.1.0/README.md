# googlesheets2csv

Export google spreadsheet to csv, you can filter data with SQL statement.

## Installation

```bash
pip install googlesheets2csv
```

### Development

```bash
git clone https://github.com/YuChunTsao/googlesheets2csv.git

cd googlesheets2csv

pip install -e .
```

## How to get credential json?

1. Create Google Cloud project.
2. Enable "Google Sheets API" and "Google Drive API".
3. Go to "APIs & Services > Credentials" and choose "CREATE CREDENTIALS > Service account".
4. Fill out the form and click "Create" and "Done".
5. Go to "IAM & Admin > Service Accounts > Keys" and click "ADD KEY > Create new key".
6. Select JSON key type and press "Create". (The file will be downloaded automatically.)

## CLI usage

```txt
usage: googlesheets2csv [-h] [-v] -c  -sn  -wn  [-sql] output

Export google spreadsheet to csv, you can filter data with SQL statement.

positional arguments:
  output                Output csv file path

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c, --credential_file 
                        Google Cloud service account JSON file with credentials
  -sn, --spreadsheet_name 
                        spreadsheet name which you want to access
  -wn, --worksheet_name 
                        worksheet name which you want to access
  -sql                  You can filter data with SQL statement. (default "SELECT * FROM your_worksheet_name")
```
