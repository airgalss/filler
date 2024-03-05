import os.path
import json
import sys

def begin_generate():
    with open(key_file, "r") as f:
        key_dict = json.load(f)

    with open(source_file, "r") as f:
        source_dict = json.load(f)

    keys = {i["key"]: "" for i in key_dict}
    for key in keys:
        if key in source_dict:
            keys[key] = source_dict[key]
            
    with open(output_file, "w") as f:
        json.dump(keys, f, indent=4)

root = os.path.normpath(os.path.dirname(__file__) + "/..")
name_list_file = f"{root}/name.json"
with open(name_list_file, "r") as f:
    name_list = json.load(f)
nlist = [ i["name"] for i in name_list ]

argc = len(sys.argv)
if argc == 1:
    print("a name must be provided")
    sys.exit(1)
elif argc == 2:
    name = sys.argv[1]
    data_dir = f"{root}/test/post_convert/"
    key_file = f"{root}/conf/{name}/field.json"
    source_file = f"{root}/tools/anchor.json"
    output_file = f"{data_dir}/{name}.json"
    if name in nlist:
        begin_generate()
    else:
        print("invalid name")
        sys.exit(1)
elif argc > 2:
    print("only an argument can be provided")
    sys.exit(1)