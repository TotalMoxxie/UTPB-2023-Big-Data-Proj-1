import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
import xmltodict
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wordcloud import WordCloud
import random
import string


data = {} # Initialize data as an empty dictionary
xml_dict = {} # Initialize xml_dict as an empty dictionary
edid_count = 0
rec_count = 0
english_count = 0
spanish_count = 0


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

#------------------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------------------
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

#-------------------------------------------------------------------
# Create a variable to store the canvas widget
pie_chart_canvas = None

# Create a function to clear the canvas
def clear_pie_canvas():
    global pie_chart_canvas
    if pie_chart_canvas:
        pie_chart_canvas.get_tk_widget().destroy()
        pie_chart_canvas = None


# Create the "Search Pie Chart" function:
def search_pie_chart():
    global data, xml_dict, pie_chart_canvas
    query = pie_search_entry.get().lower()

    # Initialize counts for each field
    edid_count = 0
    rec_count = 0
    english_count = 0
    spanish_count = 0
    total_count = 0

    if 'SSTXMLRessources' in data and 'Content' in data['SSTXMLRessources'] and 'String' in data['SSTXMLRessources'][
        'Content']:
        for entry in data['SSTXMLRessources']['Content']['String']:
            edid_count += query in entry.get('EDID', '').lower()
            rec_count += query in entry.get('REC', '')
            english_count += query in entry.get('Source', '').lower()
            spanish_count += query in entry.get('Dest', '').lower()

    if 'SSTXMLRessources' in xml_dict and 'Content' in xml_dict['SSTXMLRessources'] and 'String' in \
            xml_dict['SSTXMLRessources']['Content']:
        for entryxml in xml_dict['SSTXMLRessources']['Content']['String']:
            edid_count += query in entryxml.get('EDID', '').lower()
            rec_count += query in entryxml.get('REC', '')
            english_count += query in entryxml.get('Source', '').lower()
            spanish_count += query in entryxml.get('Dest', '').lower()

    # Calculate the total count
    total_count = edid_count + rec_count + english_count + spanish_count

    # Create pie chart data
    labels = ['EDID', 'REC', 'English', 'Spanish']
    counts = [edid_count, rec_count, english_count, spanish_count]
    percentages = [count / total_count * 100 if total_count > 0 else 0 for count in counts]
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(labels)))

    clear_pie_canvas()  # Clear the canvas if it exists

    # Create the pie chart figure and canvas
    fig = plt.Figure()
    pie_chart_canvas = FigureCanvasTkAgg(fig, pie_chart_viz)
    pie_chart_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Create pie chart axes
    ax = fig.add_subplot(111)

    # Plot the pie chart
    ax.pie(percentages, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)

    # Set the aspect ratio to be equal, so the pie is circular
    ax.axis('equal')

    # Pack the pie chart canvas
    pie_chart_canvas.draw()


# Create the Pie Chart tab
pie_chart_viz = ttk.Frame(notebook)
notebook.add(pie_chart_viz, text="Pie Chart Viz")

# Create "Pie Chart" button
#pie_chart_button = ttk.Button(visualizations, text="Pie Chart", command=search_pie_chart)
#pie_chart_button.pack()

# Create a search input field and a button
pie_search_label = ttk.Label(pie_chart_viz, text="Search:")
pie_search_label.pack(pady=10)
pie_search_entry = ttk.Entry(pie_chart_viz)
pie_search_entry.pack(pady=5)
pie_search_button = ttk.Button(pie_chart_viz, text="Search", command=search_pie_chart)
pie_search_button.pack(pady=10)

# Create the "Clear" button
clear_button = ttk.Button(pie_chart_viz, text="Clear", command=clear_pie_canvas)
clear_button.pack(pady=10)
#----------------------------------------------------------------------
# Create a function to generate stopwords for the Word Cloud
def generate_stopwords(language):
    stopwords = []
    if language == "English":
        stopwords = ["the", "and", "of", "in", "to", "for", "with", "as", "on", "by"]
    elif language == "Spanish":
        stopwords = ["el", "la", "de", "en", "para", "con", "por", "como", "una", "su"]
    return stopwords

# Create a global variable to store the Word Cloud canvas
word_cloud_canvas = None

# Function to clear the Word Cloud canvas
def clear_word_canvas():
    global word_cloud_canvas
    if word_cloud_canvas:
        word_cloud_canvas.get_tk_widget().destroy()
        word_cloud_canvas = None


# Update the generate_word_cloud function
def generate_word_cloud(language):
    global data, xml_dict, word_cloud_canvas

    # Clear the existing Word Cloud canvas
    clear_word_canvas()

    # Initialize variables to store text data for the selected language
    text_data = ""
    stopwords = []  # Initialize stopwords

    # Check if the selected language is English or Spanish
    if language == "English":
        # If English, collect text data from the 'Source' field
        if 'SSTXMLRessources' in data and 'Content' in data['SSTXMLRessources'] and 'String' in data['SSTXMLRessources']['Content']:
            for entry in data['SSTXMLRessources']['Content']['String']:
                text_data += entry.get('Source', '') + " "
        # Set English stopwords
        stopwords = ["the", "and", "of", "in", "to", "for", "with", "as", "on", "by"]
    elif language == "Spanish":
        # If Spanish, collect text data from the 'Dest' field
        if 'SSTXMLRessources' in data and 'Content' in data['SSTXMLRessources'] and 'String' in data['SSTXMLRessources']['Content']:
            for entry in data['SSTXMLRessources']['Content']['String']:
                text_data += entry.get('Dest', '') + " "
        # Set Spanish stopwords
        stopwords = ["el", "la", "de", "en", "para", "con", "por", "como", "una", "su"]

    # Remove punctuation and convert to lowercase
    text_data = "".join([char.lower() if char not in string.punctuation else " " for char in text_data])

    # Generate the Word Cloud
    wordcloud = WordCloud(width=800, height=400, stopwords=stopwords, background_color='white').generate(text_data)

    # Create a canvas to display the Word Cloud
    word_cloud_canvas = FigureCanvasTkAgg(plt.figure(figsize=(8, 4)), word_cloud_tab)
    word_cloud_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Display the Word Cloud on the canvas
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    word_cloud_canvas.draw()


# Create the Word Cloud tab
word_cloud_tab = ttk.Frame(notebook)
notebook.add(word_cloud_tab, text="Word Cloud")

# Create buttons for generating Word Cloud for English and Spanish
english_button = ttk.Button(word_cloud_tab, text="Generate English Word Cloud",
                            command=lambda: generate_word_cloud("English"))
english_button.pack(pady=10)
spanish_button = ttk.Button(word_cloud_tab, text="Generate Spanish Word Cloud",
                            command=lambda: generate_word_cloud("Spanish"))
spanish_button.pack(pady=10)

# Create a clear button to clear the Word Cloud canvas
clear_button = ttk.Button(word_cloud_tab, text="Clear Word Cloud", command=clear_word_canvas)
clear_button.pack(pady=10)
#----------------------------------------------------------------------
# Run the application
root.mainloop()
