import xmltodict
import json
import os
import tkinter as tk 
from tkinter import ttk


# proj
# make a tkinter widget that shows the data as a tree
# show a table of data
# try tkinter frame
# try tkinter treeview

# def display_tree(data, parent=''):
#     for key, value in data.items():
#         if isinstance(value, dict):
#             tree.insert(parent, 'end', text=(key))
#             display_tree(value, parent=(key))
#         else:
#             tree.insert(parent, 'end', text=key, values=(value))



path = "C:\\Users\\Everest\\Desktop\\" 
input_xml = "Dragonborn.xml" 
output_json = "Dragon.json"

xml_dict = dict()

with open(os.path.join(path, input_xml), 'r', encoding="utf8") as xml_file:
    xml_data = xml_file.read()
    xml_dict = xmltodict.parse(xml_data)

with open(os.path.join(path, output_json), 'w', encoding="utf8") as json_file:
    json.dump(xml_dict, json_file, ensure_ascii=False, sort_keys=True, indent=4)

# root = tk.Tk()
# tree = ttk.Treeview(root)
# tree.pack(fill='both', expand=True)
#
# display_tree(xml_dict)
#
# root.mainloop()

for entry in xml_dict['SSTXMLRessources']["Content"]['String']:
    if "dragon" in entry['Source'].lower():
        print(f"en: {entry['Source']} es: {entry['Dest']}")
    if "castillo" in entry['Dest'].lower():
        print(f"en: {entry['Source']} es: {entry['Dest']}")
