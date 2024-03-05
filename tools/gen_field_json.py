import os.path
import json
import sys
import fitz

def begin_generate(key="field_name"):
    with open(anchor_file, "r") as f:
        dic = json.load(f)
    reverse_dict = {value: key for key, value in dic.items()}
    output_list = []
    doc = fitz.open(example_file)
    for page in doc:
        for field in page.widgets():
            if field.field_value in reverse_dict.keys():
                if key == "field_name":
                    output_list.append({"type": "textbox",
                                        "key": reverse_dict[field.field_value],
                                        "page": page.number,
                                        "label": field.field_name
                    })
                elif key == "xref":
                    output_list.append({"type": "textbox",
                                        "key": reverse_dict[field.field_value],
                                        "page": page.number,
                                        "xref": field.xref
                    })
    with open(output_file, "w") as f:
        json.dump(output_list, f, indent=4)

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
    anchor_file = f"{root}/tools/anchor.json"
    example_file = f"{root}/tools/example/{name}.pdf"
    output_file = f"{root}/conf/{name}/field.json"
    if name in nlist:
        begin_generate(key="field_name")
    else:
        print("invalid name")
        sys.exit(1)
elif argc > 2:
    print("only an argument can be provided")
    sys.exit(1)
