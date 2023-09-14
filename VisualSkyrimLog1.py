import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import json
import os



path = "C:\\Users\\Everest\\Desktop\\"
input_xml = "Dragonborn.xml"
output_json = "Dragon.json"

# Load JSON data
with open(os.path.join(path, output_json), "r", encoding="utf8") as json_file:
    data = json.load(json_file)


def search():
    query = search_entry.get().lower()
    results_tree.delete(*results_tree.get_children())

    for entry in data['SSTXMLRessources']["Content"]['String']:
        if query in entry['Source'].lower() or query in entry['Dest'].lower():
            results_tree.insert("", "end", values=(entry['Source'], entry['Dest']))


# Create the main window
#root = tk.Tk()
root = ThemedTk(theme="arc")
root.title("Dictionary App")
root.geometry("800x600")

# Create a notebook with two tabs: Dictionary and Search
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create the Dictionary tab
dictionary_frame = ttk.Frame(notebook)
notebook.add(dictionary_frame, text="Dictionary")

# Create a Treeview widget to display the dictionary
dictionary_tree = ttk.Treeview(dictionary_frame, columns=("English", "Spanish"))
dictionary_tree.heading("#1", text="English")
dictionary_tree.heading("#2", text="Spanish")
dictionary_tree.pack(fill="both", expand=True)

# Populate the Treeview with data from the JSON file
for entry in data['SSTXMLRessources']["Content"]['String']:
    dictionary_tree.insert("", "end", values=(entry['Source'], entry['Dest']))

# Create the Search tab
search_frame = ttk.Frame(notebook)
notebook.add(search_frame, text="Search")

# Create a search input field and a button
search_label = ttk.Label(search_frame, text="Search:")
search_label.pack(pady=10)
search_entry = ttk.Entry(search_frame)
search_entry.pack(pady=5)
search_button = ttk.Button(search_frame, text="Search", command=search)
search_button.pack(pady=10)

# Create a Treeview widget to display search results
results_tree = ttk.Treeview(search_frame, columns=("English", "Spanish"))
results_tree.heading("#1", text="English")
results_tree.heading("#2", text="Spanish")
results_tree.pack(fill="both", expand=True)

# Run the application
root.mainloop()
