import os
import json
import tkinter as tk
from tkinter import filedialog, OptionMenu, Scrollbar

def load_json_file(*args):
    selected_file = selected_file_var.get()
    with open(selected_file, 'r') as f:
        data = json.load(f)
        json_text.delete(1.0, tk.END)  # Clear previous content
        json_text.insert(tk.END, json.dumps(data, indent=4))

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

json_text = tk.Text(root, wrap=tk.WORD, width=50, height=20)
json_text.grid(row=1, column=0, padx=10, pady=10)

scrollbar = Scrollbar(root, orient="vertical", command=json_text.yview)
scrollbar.grid(row=1, column=1, sticky="NS")
json_text.config(yscrollcommand=scrollbar.set)

load_json_file()  # Load JSON file initially

selected_file_var.trace_add("write", load_json_file)  # Call load_json_file when selection changes

root.mainloop()