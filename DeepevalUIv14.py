import os
import json
import tkinter as tk
from tkinter import OptionMenu, Scrollbar, ttk, Menu, filedialog

def load_json_file(*args):
    """Load JSON file and populate test cases dropdown."""
    selected_file = selected_file_var.get()
    if selected_file and selected_file != "Select File...":
        with open(selected_file, 'r') as f:
            data = json.load(f)
            test_cases = [test_case['name'] for test_case in data['testCases']]
            test_case_var.set(test_cases[0])  # Set default selection
            populate_test_cases_dropdown(test_cases)
            display_test_case_info()

def populate_test_cases_dropdown(test_cases):
    """Populate the test cases dropdown menu."""
    test_case_dropdown['menu'].delete(0, 'end')  # Clear previous menu items
    for test_case in test_cases:
        test_case_dropdown['menu'].add_command(label=test_case, command=tk._setit(test_case_var, test_case))

def display_test_case_info(*args):
    """Display selected test case information and metrics."""
    selected_test_case = test_case_var.get()
    selected_file = selected_file_var.get()
    if selected_file and selected_file != "Select File...":
        with open(selected_file, 'r') as f:
            data = json.load(f)
            for test_case in data['testCases']:
                if test_case['name'] == selected_test_case:
                    display_test_case_data(test_case)
                    display_metrics_data(test_case.get('metricsMetadata', []))
                    break

def display_test_case_data(test_case):
    """Display main test case information in the treeview."""
    test_case_tree.delete(*test_case_tree.get_children())  # Clear previous content
    
    for key, value in test_case.items():
        if key != 'metricsMetadata':
            if isinstance(value, list):  # Convert list to string for display
                value = ", ".join(map(str, value))
            test_case_tree.insert('', 'end', values=(key, value))

def display_metrics_data(metrics):
    """Display metrics information in the metrics frame."""
    for widget in metrics_frame.winfo_children():
        widget.destroy()  # Clear previous content
    
    for i, metric in enumerate(metrics):
        metric_label = tk.Label(metrics_frame, text=f"Metric {i + 1}: {metric['metric']}")
        metric_label.pack(anchor='w', padx=5, pady=2)
        
        metric_tree = ttk.Treeview(metrics_frame, columns=('Key', 'Value'), show='headings', height=5)
        metric_tree.heading('#1', text='Key')
        metric_tree.heading('#2', text='Value')
        metric_tree.column('#1', width=200, anchor='w')
        metric_tree.column('#2', width=600, anchor='w')
        metric_tree.pack(fill='x', padx=5, pady=5)
        
        for key, value in metric.items():
            if isinstance(value, list):  # Convert list to string for display
                value = ", ".join(map(str, value))
            metric_tree.insert('', 'end', values=(key, value))
        
        metric_scrollbar = Scrollbar(metrics_frame, orient="vertical", command=metric_tree.yview)
        metric_tree.configure(yscrollcommand=metric_scrollbar.set)
        metric_scrollbar.pack(side='right', fill='y')

def open_file_dialog():
    """Open file dialog to select a JSON file."""
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

metrics_frame = tk.Frame(root)
metrics_frame.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

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

# Bottom Frame: Test case data display
test_case_label = tk.Label(bottom_frame, text="Test Case Information")
test_case_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

test_case_tree = ttk.Treeview(bottom_frame, columns=('Key', 'Value'), show='headings')
test_case_tree.heading('#1', text='Key')
test_case_tree.heading('#2', text='Value')
test_case_tree.column('#1', width=200, anchor='w')
test_case_tree.column('#2', width=600, anchor='w')
test_case_tree.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

# Scrollbar for test case tree
test_case_scrollbar = Scrollbar(bottom_frame, orient="vertical", command=test_case_tree.yview)
test_case_scrollbar.grid(row=1, column=1, sticky='ns')
test_case_tree.configure(yscrollcommand=test_case_scrollbar.set)

# Bind dropdown changes to functions
selected_file_var.trace_add("write", load_json_file)
test_case_var.trace_add("write", display_test_case_info)

root.mainloop()