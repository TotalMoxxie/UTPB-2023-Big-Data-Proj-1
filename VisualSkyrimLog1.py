import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
import xmltodict
import json
from PIL import Image, ImageTk
from io import BytesIO
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots

data = {} # Initialize data as an empty dictionary
xml_dict = {} # Initialize xml_dict as an empty dictionary

# Create a function to open JSON File
def open_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r", encoding="utf8") as json_file:
            global data
            data = json.load(json_file)
        update_dictionary_tree()

# Create a function to open XML File
def open_xml_file():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        with open(file_path, 'r', encoding="utf8") as xml_file:
            global xml_data
            xml_data = xml_file.read()
            global xml_dict
            xml_dict = xmltodict.parse(xml_data)
        update_dictionary_tree_xml()

# Create the main window
root = ThemedTk(theme="arc")
root.title("Skryim Dictionary App")
root.geometry("800x600")

# Create a notebook with two tabs: Dictionary and Search
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create the Dictionary tab
dictionary_frame = ttk.Frame(notebook)
notebook.add(dictionary_frame, text="Treeview")

# Create "Open JSON" and "Open XML" buttons
open_json_button = ttk.Button(dictionary_frame, text="Open JSON", command=open_json_file)
open_json_button.grid(row=1, column=0, sticky='w')

open_xml_button = ttk.Button(dictionary_frame, text="Open XML", command=open_xml_file)
open_xml_button.grid(row=1, column=0, sticky='e')

# Create a Treeview widget to display the dictionary
dictionary_tree = ttk.Treeview(dictionary_frame, columns=("EDID","REC","English", "Spanish"), show=['headings'])
dictionary_tree.heading("#1", text="EDID")
dictionary_tree.column("#1", minwidth=100, width=100)
dictionary_tree.heading("#2", text="REC")
dictionary_tree.column("#2", minwidth=100, width=100)
dictionary_tree.heading("#3", text="English")
dictionary_tree.column("#3", minwidth=100, width=100)
dictionary_tree.heading("#4", text="Spanish")
dictionary_tree.column("#4", minwidth=100, width=100)
dictionary_tree.grid(row=0, column=0, sticky='nsew')

# Create a scrollbar for the above Treeview widget
vsb1 = ttk.Scrollbar(dictionary_frame, orient="vertical", command=dictionary_tree.yview)
vsb1.grid(row=0, column=1, sticky='ns')
dictionary_tree.configure(yscrollcommand=vsb1.set)

# Configure grid row and column weights to make the Treeview and scrollbar expand
dictionary_frame.grid_rowconfigure(0, weight=1)
dictionary_frame.grid_columnconfigure(0, weight=1)

# Function to update the dictionary_tree with the loaded JSON data
def update_dictionary_tree():
    global data
    # Clear the current contents of the dictionary_tree
    dictionary_tree.delete(*dictionary_tree.get_children())

    # Populate the Treeview with data from the loaded JSON file
    for entry in data['SSTXMLRessources']["Content"]['String']:
        dictionary_tree.insert("", "end", values=(entry['EDID'], entry['REC'], entry['Source'], entry['Dest']))

# Function to update the dictionary_tree with the loaded XML data
def update_dictionary_tree_xml():
    global xml_dict
    # Clear the current contents of the dictionary_tree
    dictionary_tree.delete(*dictionary_tree.get_children())

    # Populate the Treeview with data from the loaded XML dictionary
    if "SSTXMLRessources" in xml_dict and "Content" in xml_dict["SSTXMLRessources"] and "String" in xml_dict["SSTXMLRessources"]["Content"]:
        for entry in xml_dict["SSTXMLRessources"]["Content"]["String"]:
            dictionary_tree.insert("", "end", values=(entry.get('EDID', ''), entry.get('REC', ''), entry.get('Source', ''), entry.get('Dest', '')))

# Create the Search tab
search_frame = ttk.Frame(notebook)
notebook.add(search_frame, text="Search")

# Create a search function
def search():
    global data
    global xml_dict
    query = search_entry.get().lower()
    results = []

    # Search in JSON data
    if 'SSTXMLRessources' in data and 'Content' in data['SSTXMLRessources'] and 'String' in data['SSTXMLRessources']['Content']:
        for entry in data['SSTXMLRessources']['Content']['String']:
            if query in entry.get('EDID', '').lower() or query in entry.get('REC', '') or query in entry.get('Source', '').lower() or query in entry.get('Dest', '').lower():
                results.append((entry.get('EDID', ''), entry.get('REC', ''), entry.get('Source', ''), entry.get('Dest', '')))

    # Search in XML data
    if 'SSTXMLRessources' in xml_dict and 'Content' in xml_dict['SSTXMLRessources'] and 'String' in xml_dict['SSTXMLRessources']['Content']:
        for entryxml in xml_dict['SSTXMLRessources']['Content']['String']:
            if query in entryxml.get('EDID', '').lower() or query in entryxml.get('REC', '') or query in entryxml.get('Source', '').lower() or query in entryxml.get('Dest', '').lower():
                results.append((entryxml.get('EDID', ''), entryxml.get('REC', ''), entryxml.get('Source', ''), entryxml.get('Dest', '')))

    # Create a popup window for displaying search results
    popup = tk.Toplevel(root)
    popup.title("Search Results")
    popup.geometry("800x400")

    # Create a Treeview widget to display the search results in the popup window
    results_tree = ttk.Treeview(popup, columns=("EDID", "REC", "English", "Spanish"), show=['headings'])
    results_tree.heading("#1", text="EDID")
    results_tree.column("#1", minwidth=100, width=100)
    results_tree.heading("#2", text="REC")
    results_tree.column("#2", minwidth=100, width=100)
    results_tree.heading("#3", text="English")
    results_tree.column("#3", minwidth=100, width=100)
    results_tree.heading("#4", text="Spanish")
    results_tree.column("#4", minwidth=100, width=100)
    results_tree.grid(row=0, column=0, sticky='nsew')

    # Create a scrollbar for the above Treeview widget
    vsb2 = ttk.Scrollbar(popup, orient="vertical", command=results_tree.yview)
    vsb2.grid(row=0, column=1, sticky='ns')
    results_tree.configure(yscrollcommand=vsb2.set)

    # Configure grid row and column weights to make the Treeview and scrollbar expand
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_columnconfigure(0, weight=1)

    # Clear the current contents of the results_tree
    results_tree.delete(*results_tree.get_children())

    # Populate the Treeview with search results
    for result in results:
        results_tree.insert("", "end", values=result)

# Create a search input field and a button
search_label = ttk.Label(search_frame, text="Search:")
search_label.pack(pady=10)
search_entry = ttk.Entry(search_frame)
search_entry.pack(pady=5)
search_button = ttk.Button(search_frame, text="Search", command=search)
search_button.pack(pady=10)

# # Create the Pie Chart tab
# pie_chart_frame = ttk.Frame(notebook)
# notebook.add(pie_chart_frame, text="Pie Chart")
#
# # Function to create and display a pie chart
# def create_pie_chart():
#     # Sample data for the pie chart
#     labels = ['A', 'B', 'C', 'D']
#     values = [40, 30, 20, 10]
#
#     # Create a subplot with a pie chart using Plotly
#     fig = make_subplots(1, 1)
#     fig.add_trace(go.Pie(labels=labels, values=values, hole=0.3))
#
#     # Update layout
#     fig.update_layout(title_text='Sample Pie Chart')
#
#     # Convert the Plotly figure to an image
#     img_bytes = pio.to_image(fig, format="png")
#
#     # Display the image in a Tkinter window
#     img = Image.open(BytesIO(img_bytes))
#     img = ImageTk.PhotoImage(img)
#
#     pie_chart_window = tk.Toplevel(root)
#     pie_chart_window.title("Pie Chart")
#     pie_chart_window.geometry("800x400")
#
#     label = ttk.Label(pie_chart_window, image=img)
#     label.image = img
#     label.pack()
#
# # Add a button to create the pie chart
# piebutton = ttk.Button(pie_chart_frame, text="Create Pie Chart", command=create_pie_chart)
# piebutton.pack(pady=10)

# Run the application
root.mainloop()
