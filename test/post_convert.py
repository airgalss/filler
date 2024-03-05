import sys
sys.path.append("../../")
import json
import filler
import os.path

def begin_test(name):
    print(f"Generating filled pdf: {name}...")
    value_file = f"{curpath}/post_convert/{name}.json"
    with open(value_file, "r") as f:
        value = json.load(f)

    handler = filler.Filler(name)
    handler.fill(value, enable_convert=False)
    handler.export()

root = os.path.normpath(os.path.dirname(__file__) + "/..")
name_list_file = f"{root}/name.json"

with open(name_list_file, "r") as f:
    name_list = json.load(f)

nlist = [ i["name"] for i in name_list ]

curpath = os.path.dirname(__file__)

argc = len(sys.argv)
if argc == 1:
    for name in nlist:
        begin_test(name)
elif argc == 2:
    print(sys.argv[1])
    if sys.argv[1] in nlist:
        begin_test(sys.argv[1])
    else:
        print("invalid name")
        sys.exit(1)
elif argc > 2:
    print("only an argument can be provided")
    sys.exit(1)