# ZippyLeech
Python script to download a list of Zippyshare.com URLs. You can provide the URLs on the command line, from a plain text file (URLs separated by linebreaks), or from a DLC file.
At the end, it will list how many links were downloaded successfully, how many were skipped, and how many failed to download.

# Requirements
* Python 3.6 (or above)
  * tqdm
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
    $ python3 zipPy.py -f list.txt
    Downloading (1/2): Oblivion Song 026 (2020) (Digital) (Zone-Empire).cbr (attempt 3/3)
    Song (2020) (Digital) (HDR).mkv: 42043KB [00:06, 6457.44KB/s]  
    Downloading (2/2): []

    Summary: 2 successful, 0 failed, 0 skipped

# Changelog
## v2.2
* Ditch clint for tqdm progress bar
## v2.1
* Fix modulous calculation
## v1.0
* Initial release

