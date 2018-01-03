# zipPy
Zippyshare download script, written in Python.

Takes a list of Zippyshare.com URLs, either from a file or on the command line, and downloads them to the specified output directory (default: ./).

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
