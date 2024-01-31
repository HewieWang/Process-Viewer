import tkinter as tk
from tkinter import ttk, Menu
import psutil
import subprocess

class ProcessViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Viewer")

        self.process_tree = ttk.Treeview(root, columns=("pid", "name"), show="headings", selectmode="browse")
        self.process_tree.heading("pid", text="PID")
        self.process_tree.heading("name", text="Name")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_processes)
        self.search_entry = ttk.Entry(root, textvariable=self.search_var, width=20)

        self.context_menu = Menu(root, tearoff=0)
        self.context_menu.add_command(label="Copy PID", command=self.copy_pid)

        self.populate_processes()

        self.process_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.search_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.process_tree.bind("<Button-3>", self.show_context_menu)

    def populate_processes(self):
        for proc in psutil.process_iter(['pid', 'name']):
            pid, name = proc.info['pid'], proc.info['name']
            self.process_tree.insert("", "end", values=(pid, name))

    def filter_processes(self, *args):
        search_query = self.search_var.get().lower()
        self.process_tree.delete(*self.process_tree.get_children())
        for proc in psutil.process_iter(['pid', 'name']):
            pid, name = proc.info['pid'], proc.info['name']
            if search_query in str(pid) or search_query in name.lower():
                self.process_tree.insert("", "end", values=(pid, name))

    def show_context_menu(self, event):
        item = self.process_tree.selection()
        if item:
            self.context_menu.post(event.x_root, event.y_root)

    def copy_pid(self):
        selected_item = self.process_tree.selection()
        if selected_item:
            pid = self.process_tree.item(selected_item, "values")[0]
            self.root.clipboard_clear()
            self.root.clipboard_append(pid)
            self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessViewer(root)
    root.mainloop()
