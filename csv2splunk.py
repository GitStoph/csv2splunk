#!/usr/bin/env python3
# This script will allow you to manipulate csv data with splunk without uploading it to the splunk instance.
# 4/11/23 GitStoph
############################################################################################################

from rich.console import Console
import urllib
import argparse
import csv
import os

console = Console()

def get_args(): # creating our args to parse later.
    parser = argparse.ArgumentParser(
        description='Arguments for ingesting your csv for Splunk consumption, without having to actually ingest it into your splunk instance!')
    parser.add_argument('-i', '--instance',required=True,type=str,default='my-instance',action='store',
        help="Which instance of splunk are you looking to use? ie: my-instance.splunkcloud.com would result in passing 'my-instance'. ")
    parser.add_argument('-f', '--filepath',required=True,type=str,default='./test.csv',action='store',
        help="What is the FULL file path to the csv to be searched within splunk?")
    args = parser.parse_args()
    return args


def dictit(fpath): # imports and dicts the csv
    if os.path.isfile('{0}'.format(fpath)) == True:
        reader = csv.DictReader(open('{0}'.format(fpath)),
            delimiter=',',lineterminator='\n')
        result = [{k: v for k, v in row.items()} for row in reader]
        return result


def generate_query(listofdicts, keys):
    headerRegex = ""
    for key in keys:
        headerRegex += "(?<"+key+">.*),"
    headerTable = ""
    for key in keys:
        headerTable += key+","
    content = ""
    for each in listofdicts:
        for key in keys:
            content += each[key]+","
        content = content[:-1]
        content += ";"
    query = "| stats count as field1 | eval field1=\""+content[:-1]+"\" | eval field1=split(field1,\";\") | mvexpand field1 | rex field=field1 \""+headerRegex[:-1]+"\" | table "+headerTable[:-1]+""
    return query


def standardize_dicts(listofdicts):
    keys = []
    for each in listofdicts:
        for key in each.keys():
            if key not in keys:
                keys.append(key)
    for each in listofdicts:
        for key in keys:
            if key not in each.keys():
                each[key]="NA"
    return listofdicts, keys


def create_search_link(instance, query):
    encoded_query = urllib.parse.quote(query)
    search_link = f'https://{instance}.splunkcloud.com/en-US/app/search/search?q={encoded_query}&display.page.search.mode=verbose&dispatch.sample_ratio=1&workload_pool=standard_perf&earliest=-30m%40m&latest=now&display.page.search.tab=statistics&display.general.type=statistics'
    return search_link


def main():
    try:
        args = get_args()
        console.log(f"[green]Using the {args.instance} Splunk instance.")
        csvlist = dictit(args.filepath)
        standardized, keys = standardize_dicts(csvlist)
        query = generate_query(standardized, keys)
        search_link = create_search_link(args.instance, query)
        console.print(search_link)
    except KeyboardInterrupt:
        console.log("[red][!!!] Ctrl + C Detected!")
        console.log("[red][XXX] Exiting script now..")
        exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.log("\n[!!!] Ctrl + C Detected!")
        console.log("[XXX] Exiting script now..")
        exit()
