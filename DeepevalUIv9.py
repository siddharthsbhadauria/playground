import os
import json
import tkinter as tk
from tkinter import OptionMenu, Scrollbar, ttk

def load_json_file(*args):
    selected_file = selected_file_var.get()
    if selected_file != "Select File...":
        with open(selected_file, 'r') as f:
            data = json.load(f)
            test_cases = [test_case['name'] for test_case in data['testCases']]
            test_case_var.set(test_cases[0])  # Set default selection
            populate_test_cases_dropdown(test_cases)
            display_test_case_info()

def populate_test_cases_dropdown(test_cases):
    test_case_dropdown['menu'].delete(0, 'end')  # Clear previous menu items
    for test_case in test_cases:
        test_case_dropdown['menu'].add_command(label=test_case, command=tk._setit(test_case_var, test_case))

def display_test_case_info(*args):
    selected_test_case = test_case_var.get()
    selected_file = selected_file_var.get()
    if selected_file != "Select File...":
        with open(selected_file, 'r') as f:
            data = json.load(f)
            for test_case in data['testCases']:
                if test_case['name'] == selected_test_case:
                    display_test_case_data(test_case)
                    break

def display_test_case_data(test_case):
    tree.delete(*tree.get_children())  # Clear previous content
    for key, value in test_case.items():
        if key != 'metricsMetadata':
            tree.insert('', 'end', values=(key, value))

root = tk.Tk()
root.title("JSON Viewer")

selected_file_var = tk.StringVar(root)
test_case_var = tk.StringVar(root)

directory = "/Users/deepeval/deepeval_test_results"  # Change this to your directory

file_dropdown_label = tk.Label(root, text="Select a JSON file:")
file_dropdown_label.grid(row=0, column=0, padx=10, pady=5)

file_options = [("Select File...", "Select File...")]
file_options.extend([(f, os.path.join(directory, f)) for f in os.listdir(directory) if f.endswith('.json')])
selected_file_var.set(file_options[0][1])  # Set default selection

file_dropdown = OptionMenu(root, selected_file_var, *[option[1] for option in file_options])
file_dropdown.grid(row=0, column=1, padx=10, pady=5)

test_case_dropdown_label = tk.Label(root, text="Select a test case:")
test_case_dropdown_label.grid(row=1, column=0, padx=10, pady=5)

test_case_dropdown = OptionMenu(root, test_case_var, "")
test_case_dropdown.grid(row=1, column=1, padx=10, pady=5)

tree = ttk.Treeview(root, columns=('Key', 'Value'), show='headings')
tree.heading('#1', text='Key')
tree.heading('#2', text='Value')
tree.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

scrollbar = Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.grid(row=2, column=2, sticky="NS")
tree.configure(yscrollcommand=scrollbar.set)

load_button = tk.Button(root, text="Load JSON File", command=load_json_file)
load_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

selected_file_var.trace_add("write", load_json_file)
test_case_var.trace_add("write", display_test_case_info)

root.mainloop()