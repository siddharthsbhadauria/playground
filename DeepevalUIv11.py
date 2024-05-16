import os
import json
import tkinter as tk
from tkinter import OptionMenu, Scrollbar, ttk, Menu, filedialog

def load_json_file(*args):
    selected_file = selected_file_var.get()
    if selected_file and selected_file != "Select File...":
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
    if selected_file and selected_file != "Select File...":
        with open(selected_file, 'r') as f:
            data = json.load(f)
            for test_case in data['testCases']:
                if test_case['name'] == selected_test_case:
                    display_test_case_data(test_case)
                    break

def display_test_case_data(test_case):
    # Clear previous content
    for item in tree.get_children():
        tree.delete(item)
    
    # Display main test case information
    for key, value in test_case.items():
        if key != 'metricsMetadata':
            if isinstance(value, list):  # Convert list to string for display
                value = ", ".join(map(str, value))
            tree.insert('', 'end', values=(key, value))
    
    # Display metrics information
    tree.insert('', 'end', values=("Metrics", ""))
    for metric in test_case.get('metricsMetadata', []):
        for key, value in metric.items():
            if isinstance(value, list):  # Convert list to string for display
                value = ", ".join(map(str, value))
            tree.insert('', 'end', values=(f"  {key}", value))

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        selected_file_var.set(file_path)
        load_json_file()

root = tk.Tk()
root.title("JSON Viewer")

# Create menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Add file menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file_dialog)

# Create main frames
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

middle_frame = tk.Frame(root)
middle_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

bottom_frame = tk.Frame(root)
bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

# Top Frame: File selection
file_dropdown_label = tk.Label(top_frame, text="Select a JSON file:")
file_dropdown_label.grid(row=0, column=0, padx=5, pady=5)

file_options = [("Select File...", "Select File...")]
directory = "/Users/deepeval/deepeval_test_results"  # Change this to your directory
file_options.extend([(f, os.path.join(directory, f)) for f in os.listdir(directory) if f.endswith('.json')])
selected_file_var = tk.StringVar(root)
selected_file_var.set(file_options[0][1])  # Set default selection

file_dropdown = OptionMenu(top_frame, selected_file_var, *[option[1] for option in file_options])
file_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

# Middle Frame: Test case selection
test_case_dropdown_label = tk.Label(middle_frame, text="Select a test case:")
test_case_dropdown_label.grid(row=0, column=0, padx=5, pady=5)

test_case_var = tk.StringVar(root)
test_case_dropdown = OptionMenu(middle_frame, test_case_var, "")
test_case_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

# Bottom Frame: Data display
tree = ttk.Treeview(bottom_frame, columns=('Key', 'Value'), show='headings')
tree.heading('#1', text='Key')
tree.heading('#2', text='Value')
tree.column('#1', width=200, anchor='w')
tree.column('#2', width=600, anchor='w')
tree.pack(side='left', fill='both', expand=True)

scrollbar = Scrollbar(bottom_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side='right', fill='y')
tree.configure(yscrollcommand=scrollbar.set)

# Bind dropdown changes to functions
selected_file_var.trace_add("write", load_json_file)
test_case_var.trace_add("write", display_test_case_info)

root.mainloop()