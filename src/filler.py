import fitz
import json
import os.path
import sys
from filler.src.converter import *

class Filler:
    def __init__(self, name):
        self.name = name
        self.root = os.path.normpath(__file__ + "/../..")
        field_file = f"{self.root}/conf/{name}/field.json"
        default_file = f"{self.root}/conf/{name}/default.json"
        template_file = f"{self.root}/conf/{name}/template.pdf"
        
        self.doc_bak = fitz.open(template_file)
        with open(field_file, "r") as f:
            self.field = json.load(f)
        with open(default_file, "r") as f:
            self.value = json.load(f)
        
        self.map = {}
        for page in self.doc_bak:
            for field in page.widgets():
                if field.field_name not in self.map:
                    self.map[field.field_name] = field.xref
                else:
                    if isinstance(self.map[field.field_name], list):
                        self.map[field.field_name].append(field.xref)
                    else:
                        res = [self.map[field.field_name]]
                        res.append(field.xref)
                        self.map[field.field_name] = res

    @staticmethod
    def get_another(array, exclude):
        for element in array:
            if element != exclude:
                return "/" + element
    
    def get_xref(self, widget):
        if "label" in widget:
            label = widget["label"]
            if isinstance(label, str):
                return self.map[label] if label in self.map else None
            elif isinstance(label, list):
                return [ self.map[l] if l in self.map else None for l in label ]
            else:
                return None
        elif "xref" in widget:
            return widget["xref"]
        else:
            return None
    
    def click_button(self, pageno, xref, status):
        off_str = "/Off"
        if status:
            page = self.doc.load_page(pageno)
            on = page.load_widget(xref).button_states()['normal']
            on_str = "/On" if on == None else self.get_another(on, "Off")
            self.doc.xref_set_key(xref, "AS", on_str)
        else:
            self.doc.xref_set_key(xref, "AS", off_str)
       
    def fill(self, value, enable_convert=True):
        self.doc = self.doc_bak
        if not isinstance(value, dict):
            raise TypeError("Unsupported argument types")
        if enable_convert:
            value = convert(self.name, value)
        self.value.update(value)
        
        for widget in self.field:
            type = widget["type"]
            key = widget["key"]
            pageno = widget["page"]
            xref = self.get_xref(widget)
            # print(f"{key}: {xref}")
            if not xref:
                continue

            if type == "textbox" and key in self.value:
                page = self.doc.load_page(pageno)
                w = page.load_widget(xref)
                v = self.value[key]
                w.field_value = str(v) if v else ""
                w.update()
                
            elif type == "checkbox" and key in self.value:
                assert isinstance(self.value[key], list), "%s should be a list" % key
                for idx in range(len(pageno)):
                    self.click_button(pageno[idx], xref[idx], widget["option"][idx] in self.value[key])
                    
            elif type == "radiobutton" and key in self.value:
                assert isinstance(self.value[key], str), "%s should be a string" % key
                for idx in range(len(pageno)):
                    self.click_button(pageno[idx], xref[idx], widget["option"][idx] == self.value[key])
            
            elif type == "replace_text" and key in self.value:
                assert isinstance(self.value[key], str), "%s should be a str value" % key
                page = self.doc.load_page(widget["page"])
                quad = page.search_for(widget["target"], quads=True)[widget["index"]]
                shrink_height = widget.get("shrink_height", 0)
                fontname = widget.get("font-family", 'helv')
                fill = widget.get("background-color", [1, 1, 1])
                bias = widget.get("bias", [0, 0])
                fontsize = widget.get("font-size", quad.height)
                redact_quad = fitz.Quad(quad.ul, quad.ur, fitz.Point(quad.ll.x, quad.ll.y - shrink_height),
                                         fitz.Point(quad.lr.x, quad.lr.y - shrink_height))
                page.add_redact_annot(redact_quad, fill=fill)
                page.apply_redactions()
                point = fitz.Point(quad.ll.x + bias[0], quad.ll.y + bias[1])
                page.insert_text(point, self.value[key], fontsize=fontsize, fontname=fontname)
    
    def export(self, path=None):
        if not path:
            path = f"{self.root}/output/{self.name}.pdf"
        self.doc.save(path)
        self.doc.close()