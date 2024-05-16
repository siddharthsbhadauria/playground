import os
import tkinter as tk
import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def update_listbox():
    directory = '/Users/deepeval/deepeval_test_results'
    files = os.listdir(directory)
    listbox.delete(0, 'end')
    for file in files:
        listbox.insert('end', file)

def display_json(event):
    selected_index = listbox.curselection()[0]
    selected_file = listbox.get(selected_index)
    selected_file_path = os.path.join('/Users/deepeval/deepeval_test_results', selected_file)
    data = load_json(selected_file_path)
    json_display.delete(1.0, 'end')
    json_display.insert('end', json.dumps(data, indent=4))

root = tk.Tk()
root.title("JSON Viewer")

listbox = tk.Listbox(root, height=10, width=50)
listbox.pack()

load_button = tk.Button(root, text="Load Files", command=update_listbox)
load_button.pack()

listbox.bind('<<ListboxSelect>>', display_json)

json_display = tk.Text(root, height=20, width=50)
json_display.pack()

root.mainloop()