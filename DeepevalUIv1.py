import os
import tkinter as tk
from tkinter import filedialog
import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def update_dropdown():
    directory = '/Users/deepeval/deepeval_test_results'
    files = os.listdir(directory)
    dropdown['menu'].delete(0, 'end')
    for file in files:
        dropdown['menu'].add_command(label=file, command=tk._setit(selected_file, file))

def display_json():
    selected_file_path = os.path.join('/Users/deepeval/deepeval_test_results', selected_file.get())
    data = load_json(selected_file_path)
    json_display.delete(1.0, 'end')
    json_display.insert('end', json.dumps(data, indent=4))

root = tk.Tk()
root.title("JSON Viewer")

selected_file = tk.StringVar(root)
selected_file.set("Select a file")

dropdown = tk.OptionMenu(root, selected_file, "Select a file")
dropdown.pack()

load_button = tk.Button(root, text="Load Files", command=update_dropdown)
load_button.pack()

show_button = tk.Button(root, text="Show JSON", command=display_json)
show_button.pack()

json_display = tk.Text(root, height=20, width=50)
json_display.pack()

root.mainloop()