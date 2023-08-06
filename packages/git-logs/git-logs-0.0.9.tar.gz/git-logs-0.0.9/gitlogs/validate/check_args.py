from datetime import datetime 

from gitlogs.utils.bcolors import bcolors

def check_date(date):
    if (date==""):
        return True
    try:
        bool(datetime.strptime(date, "%Y-%m-%d"))
        return True
    except:
        return False


def check_frequency(f):
    if (f not in ["","day","week","month","year"]) or (not isinstance(f,str)): 
        return False 
    return True

def check_author(a):
    if(not isinstance(a,str)):
        return False
    return True

def check_reverse(r):
    if(not isinstance(r,bool)):
        return False
    return True

def check_symbol(s):
    if(not isinstance(s,str) or len(s)>1):
        return False 
    return True

def validate(before_date="", after_date="",frequency="day", author="",reverse=False,symbol="-"):
    
    if(not check_date(before_date)):
        print(bcolors.fail("Invalid date format given for --before. Format should be YYYY-MM-DD"))
        return False

    if(not check_date(after_date)):
        print(bcolors.fail("Invalid date format given for --after. Format should be YYYY-MM-DD"))
        return False
    
    if(not check_frequency(frequency)):
        print(bcolors.fail("Invalid value given for frequency. --frequency should be one of these values: day, week, month, year"))
        return False

    if(not check_author(author)):
        print(bcolors.fail("--author should be a string"))
        return False

    if(not check_reverse(reverse)):
        print(bcolors.fail("--reverse should be a boolean value(True/False)"))
        return False

    if(not check_symbol(symbol)):
        print(bcolors.fail("symbol should be a string of length 1"))
        return False

    return True