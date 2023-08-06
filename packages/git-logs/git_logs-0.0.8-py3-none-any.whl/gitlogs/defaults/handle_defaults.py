import json
import os
import inspect

from gitlogs.utils.bcolors import bcolors

here = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

def current_symbol():
    with open(f"{here}/defaults.json", 'r') as openfile:
        json_object = json.load(openfile)
        return json_object.get("SYMBOL")

def change_symbol(s):
    temp_dict = {
        "SYMBOL":s
    }
    with open(f"{here}/defaults.json", "w") as f:
        json.dump(temp_dict,f,indent="\t")

def display_symbol():
    with open(f"{here}/defaults.json", 'r') as openfile:
        json_object = json.load(openfile)
        print("Default symbol for display bar changed to %s" % bcolors.ok(json_object.get("SYMBOL")))

