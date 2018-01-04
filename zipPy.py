import requests
import sys
from re import match
from urllib import unquote
from clint.textui import progress
from optparse import OptionParser
import os

option_parser = OptionParser(usage="Usage: %prog [options] [url1] [url2] ...")
option_parser.add_option('-f', '--file', action='store', dest='url_list_file',
                         help='FILE containing a list of Zippyshare.com URLs separated by newlines', metavar='FILE')
option_parser.add_option('-o', '--output', action='store', dest='output_dir', default='./',
                         help='DIRECTORY to save downloaded files to', metavar='/path/to/destination/')
(options, args) = option_parser.parse_args()
url_list_file = options.url_list_file
output_dir = options.output_dir
if len(args) == 0:
    try:
        url_list_file = open(options.url_list_file, 'r')
        url_list = url_list_file.read().strip().split('\n')
        url_list_file.close()
    except:
        sys.exit('ERROR: Could not read URL list file: %s' % options.url_list_file)
else:
    if options.url_list_file:
        sys.exit('ERROR: Please either specify URLs on the command-line, or use -f/--file, not both.')
    url_list = args

if options.output_dir[-1] != '/':
    output_dir += '/'


successes = 0
failures = 0
skips = 0
for url in url_list:
    try:
        landing_page = requests.get(url)
    except:
        print 'Skipping invalid URL: %s' % (url)
        continue
    cookies = landing_page.cookies
    url_info = match('http://(\w+)\.zippyshare\.com/v/(\w+)/file.html', url).groups()
    subdomain = url_info[0]
    fileID = url_info[1]
    landing_page_content = landing_page.text.split('\n')
    for line in landing_page_content:
        if "document.getElementById('dlbutton').href" in line:
            try:
                page_parser = match('\s*document\.getElementById\(\'dlbutton\'\)\.href = "/([p]?d)/\w+/" \+ \((.*?)\) \+ "/(.*)";', line).groups()
            except:
                print '***** ERROR DOWNLOADING: %s\nFAILED TO PARSE DOWNLOAD URL FROM: %s' % (url, line)
                failures += 1
                break  # jump to next URL in the list
            url_subfolder = page_parser[0]
            modulo_string = eval(page_parser[1])
            file_url = page_parser[2]
            filename = unquote(file_url).decode()
            if os.path.isfile(output_dir+filename):
                skips += 1
                print 'File already exists, skipping: %s' % (filename)
                break
            download_url = 'http://%s.zippyshare.com/%s/%s/%i/%s' % (subdomain, url_subfolder, fileID, modulo_string, file_url)
            downloading = True
            attempt_number = 1
            while downloading:
                print 'Downloading: %s (attempt #%i)' % (filename, attempt_number)
                try:
                    file_download = requests.get(download_url, stream=True, cookies=cookies)
                    path = '%s%s' % (output_dir, filename)
                    with open(path, 'wb') as f:
                        total_length = int(file_download.headers.get('content-length'))
                        for chunk in progress.bar(file_download.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                    downloading = False
                    successes += 1
                except:
                    if attempt_number < 3:
                        attempt_number += 1
                    else:
                        failures += 1
                        print 'FAILED! Removing temp file'
                        print 'Failed landing page URL: %s' % (url)
                        print 'Failed download URL: %s' % (download_url)
                        try:
                            os.remove(path)
                        except:
                            pass
                        print 'Moving to next URL...'
                        downloading = False
print '\nSummary: %i successful, %i failed, %i skipped' % (successes, failures, skips)
