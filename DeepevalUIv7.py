import os
import json
import tkinter as tk
from tkinter import filedialog, OptionMenu, Scrollbar, ttk

def load_json_file(*args):
    selected_file = selected_file_var.get()
    with open(selected_file, 'r') as f:
        data = json.load(f)
        # Clear previous content
        for item in tree.get_children():
            tree.delete(item)
        # Insert JSON data into treeview
        insert_json_data("", data)

def insert_json_data(parent, data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                item = tree.insert(parent, 'end', text=key)
                insert_json_data(item, value)
            else:
                tree.insert(parent, 'end', text=key, values=(value,))
    elif isinstance(data, list):
        for item in data:
            insert_json_data(parent, item)

def populate_file_list():
    directory = "/Users/deepeval/deepeval_test_results"
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    file_options = [os.path.join(directory, file) for file in files]
    return file_options

root = tk.Tk()
root.title("JSON Viewer")

file_options = populate_file_list()
selected_file_var = tk.StringVar(root)
selected_file_var.set(file_options[0])  # Set default selection

file_dropdown = OptionMenu(root, selected_file_var, *file_options)
file_dropdown.grid(row=0, column=0, padx=10, pady=10)

tree = ttk.Treeview(root, columns=('Value',), show='tree')
tree.grid(row=1, column=0, padx=10, pady=10)
tree.heading('#0', text='Key')
tree.heading('Value', text='Value')

scrollbar = Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.grid(row=1, column=1, sticky="NS")
tree.configure(yscrollcommand=scrollbar.set)

load_json_file()  # Load JSON file initially

selected_file_var.trace_add("write", load_json_file)  # Call load_json_file when selection changes

root.mainloop()