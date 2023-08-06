import argparse

from . import __version__

args_parser = argparse.ArgumentParser(
    description="Display information from .git")

args_parser.add_argument("-v", "--version", action="store_true",
                         help="Check installed version of the package")

args_parser.add_argument("-f", "--frequency", action="store", dest="frequency",
                         type=str, required=False, default="month")

args_parser.add_argument("-u", "--author", action="store", dest="author",
                         type=str, required=False, default="",
                         help="filter by author's e-mail (substring)")

args_parser.add_argument("-a", "--after", action="store", dest="after",
                         type=str, required=False, default="",
                         help="after date (yyyy-mm-dd hh:mm)")

args_parser.add_argument("-b", "--before", action="store", dest="before",
                         type=str, required=False, default="",
                         help="before date (yyyy-mm-dd hh:mm)")

args_parser.add_argument("-r", "--reverse", action="store_true",
                         help="reverse date order")

args_parser.add_argument("-s", "--symbol", action="store",dest="symbol",type=str,default="",
                         help="change the style of display bar")

args = args_parser.parse_args()