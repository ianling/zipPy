#!/usr/bin/env python3
VERSION = '2.0'

from clint.textui import progress
from dcryptit import read_dlc
from optparse import OptionParser
from os import remove
from os.path import isfile, getsize
from re import match
from requests import get
from sys import exit
from urllib.parse import unquote


option_parser = OptionParser(usage="Usage: %prog [options] [url1] [url2] ...", version=f"%%prog v{VERSION}")
option_parser.add_option('-f', '--file', action='store', dest='url_list_file',
                         help='Path to FILE containing a list of Zippyshare.com URLs separated by newlines', metavar='FILE')
option_parser.add_option('-d', '--dlc', action='store', dest='dlc_file',
                         help='Path or URL to DLC FILE containing a list of Zippyshare.com URLs', metavar='DLC FILE')
option_parser.add_option('-o', '--output', action='store', dest='output_dir', default='./',
                         help='DIRECTORY to save downloaded files to', metavar='/path/to/destination/')
(options, args) = option_parser.parse_args()
url_list_file = options.url_list_file
dlc_file = options.dlc_file
output_dir = options.output_dir
# make sure that output path ends with a '/'
if output_dir[-1] != '/':
    output_dir += '/'

# build the list of URLs.
# include any URLs that were entered directly on the command line
url_list = args
if dlc_file:
    if dlc_file.startswith("https://") or dlc_file.startswith("http://"):
        url_list += read_dlc(url=dlc_file)
    else:
        url_list += read_dlc(path=dlc_file)
if url_list_file:
    with open(url_list_file, 'r') as url_list_file:
        url_list += url_list_file.read().strip().split('\n')

for url in list(url_list):
    if ('http:' not in url and 'https:' not in url) or url == None:
        url_list.remove(url)
total_urls = len(url_list)
if total_urls == 0:
    print('ERROR: No URLs found!')
    option_parser.print_help()
    exit()

# main downloading loop
successes = 0
failures = 0
skips = 0
max_attempts = 3
current_url_number = 0
for url in url_list:
    attempts = 0
    current_url_number += 1
    finished_download = False
    skipped = False
    while attempts <= max_attempts and not finished_download and not skipped:
        attempts += 1
        try:
            subdomain, file_id = match('http[s]?://(\w+)\.zippyshare\.com/v/(\w+)/file.html', url).groups()
        except:
            print(f'Failed to parse URL, skipping: {repr(url)}')
            skipped = True
            continue
        try:
            landing_page = get(url)
        except:
            print('Could not GET URL: {url}')
            continue
        cookies = landing_page.cookies
        landing_page_content = landing_page.text.split('\n')
        for line in landing_page_content:
            if finished_download:
                break
            if "document.getElementById('dlbutton').href" in line:
                try:
                    page_parser = match('\s*document\.getElementById\(\'dlbutton\'\)\.href = "/([p]?d)/\w+/" \+ \((.*?)\) \+ "/(.*)";', line).groups()
                except:
                    print(f"***** ERROR DOWNLOADING: {url})")
                    print(f"FAILED TO PARSE DOWNLOAD URL FROM: {line}")
                    break
                # TODO: download URLs sometimes have /pd/ instead of /d/, I am not sure why yet. This causes downloads to fail
                url_subfolder = page_parser[0].replace('pd', 'd')
                modulo_string = eval(page_parser[1])
                file_url = page_parser[2]
                filename = unquote(file_url)
                path = output_dir + filename
                if isfile(path):
                    if getsize(path) == 0:
                        print('File already exists, but size is 0 bytes. Deleting empty file and continuing download...')
                        remove(path)
                    else:
                        print(f'File already exists, skipping: {filename}')
                        skipped = True
                        break
                download_url = f'https://{subdomain}.zippyshare.com/{url_subfolder}/{file_id}/{modulo_string}/{file_url}'
                while not finished_download:
                    print(f'Downloading ({current_url_number}/{total_urls}): {filename} (attempt {attempts}/{max_attempts})')
                    try:
                        file_download = get(download_url, stream=True, cookies=cookies)
                        with open(path, 'wb') as f:
                            total_length = int(file_download.headers.get('content-length'))
                            for chunk in progress.bar(file_download.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
                        finished_download = True
                        successes += 1
                    except:
                        attempts += 1
                        break
    if not finished_download and not skipped:
        failures += 1
        print('FAILED! Removing temp file')
        print('Failed landing page URL: {url}')
        print('Failed download URL: {download_url}')
        try:
            remove(path)
        except:
            pass
        print('Moving to next URL...')
    if skipped:
        skips += 1


print(f'\nSummary: {successes} successful, {failures} failed, {skips} skipped')
