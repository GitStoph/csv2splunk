# csv2splunk
For searching/manipulating csv data within your splunk instance without ingesting the data.

## Installation:
```
git clone git@github.com:GitStoph/csv2splunk.git
cd csv2splunk
python3 -m venv venv
source venv/bin/activate
python3 -m pip install rich
chmod +x csv2splunk.py
```
If you'd prefer to use the script outside of a virtual environment, skip the venv creation, and just globally install `rich`. 

## Usage:
```
./csv2splunk.py -h
usage: csv2splunk.py [-h] -i INSTANCE -f FILEPATH

Arguments for ingesting your csv for Splunk consumption, without having to actually ingest it into your splunk instance!

optional arguments:
  -h, --help            show this help message and exit
  -i INSTANCE, --instance INSTANCE
                        Which instance of splunk are you looking to use? ie: my-instance.splunkcloud.com would result in passing 'my-instance'.
  -f FILEPATH, --filepath FILEPATH
                        What is the FULL file path to the csv to be searched within splunk?
```
Example: `./csv2splunk.py -i my-instance -f /Users/myuser/csv2splunk/test.csv`
Copy and paste the resulting hyperlink it generates into your browser. Profit. 
