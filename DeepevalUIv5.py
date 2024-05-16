import os
import json
import tkinter as tk
from tkinter import filedialog, Text, StringVar, OptionMenu

def load_json_file(*args):
    selected_file = file_var.get()
    with open(selected_file, 'r') as f:
        data = json.load(f)
        json_text.delete(1.0, tk.END)  # Clear previous content
        json_text.insert(tk.END, json.dumps(data, indent=4))

def populate_file_dropdown():
    directory = "/Users/deepeval/deepeval_test_results"
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    return [os.path.join(directory, file) for file in files]

root = tk.Tk()
root.title("JSON Viewer")

file_var = StringVar(root)
file_var.set("Select a file")

file_dropdown = OptionMenu(root, file_var, *populate_file_dropdown(), command=load_json_file)
file_dropdown.grid(row=0, column=0, padx=10, pady=10)

json_text = Text(root, wrap=tk.WORD, width=50, height=20)
json_text.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()