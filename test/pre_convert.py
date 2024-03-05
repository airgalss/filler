import sys
sys.path.append("../../")
import json
import filler
import os.path

root = os.path.normpath(os.path.dirname(__file__) + "/..")
name_list_file = f"{root}/name.json"

with open(name_list_file, "r") as f:
    name_list = json.load(f)

nlist = [ i["name"] for i in name_list ]

curpath = os.path.dirname(__file__)
value_file = f"{curpath}/pre_convert/general.json"
with open(value_file, "r") as f:
    value = json.load(f)

for name in nlist:
    handler = filler.Filler(name)
    handler.fill(value)
    handler.export()