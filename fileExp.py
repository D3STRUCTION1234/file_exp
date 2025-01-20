import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

class FileExplorer:
    def __init__(self, path):
        self.path = path
        self.files = []
        self.dirs = []
        self.explore()
    
    def explore(self):
        self.files = []
        self.dirs = []
        for root, dirs, files in os.walk(self.path):
            self.dirs.extend(dirs)
            self.files.extend(files)
            break  # Only explore the top directory

    def get_files(self):
        return self.files

class FileExplorerGUI(FileExplorer):
    def __init__(self, path):
        super().__init__(path)
        self.root = tk.Tk() 
        self.root.title("File Explorer")
        self.root.configure(background="black")
        self.create_widgets()
        self.move_state = False
        self.move_1 = None
        self.move_2 = None
        self.root.mainloop()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Files and Directories", fg="white", bg="black")
        self.label.pack()

        self.search_entry = tk.Entry(self.root, bg="black", fg="white")
        self.search_entry.pack()
        self.search_entry.bind("<Return>", lambda event: self.search_files())

        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack()

        self.search_button = tk.Button(button_frame, text="Search", command=self.search_files, bg="black", fg="white", relief="sunken")
        self.search_button.pack(side=tk.LEFT)

        self.open_button = tk.Button(button_frame, text="Open", command=self.open_file, bg="black", fg="white")
        self.open_button.pack(side=tk.LEFT)

        self.up_button = tk.Button(button_frame, text="Back", command=self.go_up_directory, bg="black", fg="white")
        self.up_button.pack(side=tk.LEFT)

        self.move_button = tk.Button(button_frame, text="Move", command=self.move_file, bg="black", fg="white")
        self.move_button.pack(side=tk.LEFT)


        self.del_button = tk.Button(button_frame, text="Delete", command=self.delete_file, bg="black", fg="white")
        self.del_button.pack(side=tk.LEFT)

        self.rename_file = tk.Button(button_frame, text="Rename", command=self.rename_file, bg="black", fg="white")
        self.rename_file.pack(side=tk.LEFT)
        
        self.new_file = tk.Button(button_frame, text="New File", command=self.new_file, bg="black", fg="white")
        self.new_file.pack(side=tk.LEFT)

        self.listbox = tk.Listbox(self.root, bg="black", fg="white")
        self.listbox.pack(fill=tk.BOTH, expand=1)
        
        self.populate_listbox()

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for dir in self.dirs:
            self.listbox.insert(tk.END, f"📁 {dir}")
        for file in self.files:
            self.listbox.insert(tk.END,f"📝{file}")

    def search_files(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term")
            return

        results = []
        for root, dirs, files in os.walk("C:\\"):  # Search the entire C: drive
            for file in files:
                if search_term.lower() in file.lower():
                    results.append(os.path.join(root, file))
        self.listbox.delete(0, tk.END)
        for result in results:
            self.listbox.insert(tk.END, result)

    def open_file(self, selection=None):
        if selection is None:
            selected = self.listbox.curselection()
        else:
            selected = selection
        if selected:
            item = self.listbox.get(selected[0])
            if item.startswith("📁 "):
                item = item[2:]
            elif item.startswith("📝 "):
                item = item[2:]
            filepath = os.path.join(self.path, item)
            if os.path.isfile(filepath):
                os.startfile(filepath)
            elif os.path.isdir(filepath):
                self.path = filepath
                self.explore()
                self.populate_listbox()

    def go_up_directory(self):
        self.path = os.path.dirname(self.path)
        self.explore()
        self.populate_listbox()

    def move_file(self):
        if not self.move_state:
            self.move_1 = self.listbox.get(self.listbox.curselection())
            if self.move_1.startswith("📝") or self.move_1.startswith("📁 "):
                self.move_1 = self.move_1[1:]
            self.move_1 = os.path.join(self.path, self.move_1)
            self.move_state = True
            messagebox.showinfo("Move", "Select the destination folder")
        else:
            self.move_2 = self.listbox.get(self.listbox.curselection())
            if self.move_2.startswith("📁 "):
                self.move_2 = self.move_2[2:]
            self.move_2 = os.path.join(self.path, self.move_2)
            if os.path.isdir(self.move_2):
                try:
                    print(f"Moving from: {self.move_1} to {self.move_2}")  # Debugging information
                    shutil.move(self.move_1, self.move_2)
                    messagebox.showinfo("Move", "File moved successfully")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to move file: {e}")
            else:
                messagebox.showerror("Error", "Destination must be a directory")
            self.move_state = False
            self.explore()
            self.populate_listbox()
    
    def delete_file(self):
        os.remove(os.path.join(self.path,self.listbox.get(self.listbox.curselection())[1:] if self.listbox.get(self.listbox.curselection()).startswith("📝") else self.listbox.get(self.listbox.curselection())[2:]))
        self.explore()
        self.populate_listbox()

    def rename_file(self):      
        os.rename(os.path.join(self.listbox.get(self.listbox.curselection())[1:] if self.listbox.get(self.listbox.curselection()).startswith("📝") else self.listbox.get(self.listbox.curselection())[2:]), self.search_entry.get())
        self.explore() 
        self.populate_listbox()

    def new_file(self):
        path = os.path.join(self.path, self.search_entry.get())
        f = open(path,"x")
        self.explore()
        self.populate_listbox()

if __name__ == "__main__":
    initial_path = "C:\\Users"
    if initial_path:
        FileExplorerGUI(initial_path)
    else:
        print("No directory selected")   