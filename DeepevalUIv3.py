import os
import json
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar

def load_json_file():
    selected_file = file_listbox.get(file_listbox.curselection())
    with open(selected_file, 'r') as f:
        data = json.load(f)
        json_text.delete(1.0, tk.END)  # Clear previous content
        json_text.insert(tk.END, json.dumps(data, indent=4))

def populate_file_list():
    directory = "/Users/deepeval/deepeval_test_results"
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    for file in files:
        file_listbox.insert(tk.END, os.path.join(directory, file))

root = tk.Tk()
root.title("JSON Viewer")

file_listbox = Listbox(root, width=50, height=10)
file_listbox.grid(row=0, column=0, padx=10, pady=10)

scrollbar = Scrollbar(root, orient="vertical")
scrollbar.grid(row=0, column=1, sticky="NS")
scrollbar.config(command=file_listbox.yview)

file_listbox.config(yscrollcommand=scrollbar.set)

populate_file_list()

file_listbox.bind("<<ListboxSelect>>", lambda event: load_json_file())

json_text = tk.Text(root, wrap=tk.WORD, width=50, height=20)
json_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()