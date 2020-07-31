# zipPy
Zippyshare download script, written in Python.

Downloads a list of Zippyshare.com URLs. You can provide the URLs on the command line, from a plain text file (URLs separated by linebreaks), or from a DLC file.

At the end, it will list how many links were downloaded successfully, how many were skipped, and how many failed to download.

If any downloads failed and you want to try them again, simply re-run the same command. zipPy will automatically detect if a file was already downloaded (based on file name) and skip it, so you will not end up with duplicate files.

# Requirements
* Python 3.6 (or above)
  * clint
  * requests
  * dcryptit>=2.0 (https://github.com/ianling/dcryptit-python)

Install dependencies automatically with pip:

    pip3 install -r requirements.txt

# Usage
    $ python3 zipPy.py -h
    Usage: zipPy.py [options] [url1] [url2] ...
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  Path to FILE containing a list of Zippyshare.com URLs
                            separated by newlines
      -d DLC FILE, --dlc=DLC FILE
                            Path or URL to DLC FILE containing a list of
                            Zippyshare.com URLs
      -o /path/to/destination/, --output=/path/to/destination/
                            DIRECTORY to save downloaded files to

# Example
    $ cat list.txt
    http://www20.zippyshare.com/v/xxxxxxxx/file.html
    http://www20.zippyshare.com/v/xxxyyyyx/file.html
    http://www20.zippyshare.com/v/xxxyyxxx/file.html
    http://www20.zippyshare.com/v/xxy3xxxx/file.html
    http://www20.zippyshare.com/v/xyyxxxxx/file.html
    $ python3 zipPy.py -f list.txt
    Downloading (1/5): Some.File.7z.001 (attempt 1/3)
    [################################] 512000/512001 - 00:05:52
    Downloading (2/5): {...}
    
    Summary: 5 successful, 0 failed, 0 skipped
    $ 

# Changelog
## v2.0
* Python3 support
* General code clean-up
## v1.4
* Changed download flow, so re-attempting downloads actually works now
* Added a little bit more error handling
* If the file already exists, check if the size is 0 bytes. If it is, overwrite it.
## v1.3
* A small bug fix where I misremembered how a Python feature worked. The bug was related to reading DLC files.
## v1.2
* Some small QoL changes, including making the output prettier.
## v1.1
* Added support for DLC files
* A couple other QOL additions for debugging and troubleshooting
## v1.0
* Initial release

