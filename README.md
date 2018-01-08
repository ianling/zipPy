# zipPy
Zippyshare download script, written in Python.

Takes a list of Zippyshare.com URLs, either from a file or on the command line, and downloads them to the specified output directory (default: ./).

At the end, it will list how many links were downloaded successfully, how many were skipped, and how many failed to download.

If any downloads failed and you want to try them again, simply re-run the same command. zipPy will automatically detect if a file was already downloaded (based on file name) and skip it, so you will not end up with duplicate files.

# Requirements
* Python 2
  * clint
  * requests
  * dcryptit (https://github.com/ianling/dcryptit-python)

# Usage
    $ python zipPy.py -h
    Usage: zipPy.py [options] [url1] [url2] ...
    
    Options:
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  FILE containing a list of Zippyshare.com URLs
                            separated by newlines
      -o /path/to/destination/, --output=/path/to/destination/
                            DIRECTORY to save downloaded files to
                            
# Example
    $ cat list.txt
    http://www20.zippyshare.com/v/xxxxxxxx/file.html
    http://www20.zippyshare.com/v/xxxyyyyx/file.html
    http://www20.zippyshare.com/v/xxxyyxxx/file.html
    http://www20.zippyshare.com/v/xxy3xxxx/file.html
    http://www20.zippyshare.com/v/xyyxxxxx/file.html
    $ python zipPy -f list.txt
