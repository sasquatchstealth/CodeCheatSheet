import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb  # Dark theme



DB_FILE = "commands.db"

def fetch_commands():
    lang_filter = language_var.get()
    keyword = search_var.get().lower()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT description, command FROM commands WHERE 1=1"
    params = []
    
    if lang_filter and lang_filter != "All":
        query += " AND language = ?"
        params.append(lang_filter)

    if keyword:
        query += " AND LOWER(description) LIKE ?"
        params.append(f"%{keyword}%")

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    result_tree.delete(*result_tree.get_children())  

    for row in results:
        result_tree.insert("", "end", values=row)

def add_command():
    lang = language_entry.get()
    cmd = command_entry.get()
    desc = description_entry.get()

    if not lang or not cmd or not desc:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO commands (language, command, description) VALUES (?, ?, ?)", (lang, cmd, desc))
    conn.commit()
    conn.close()

    fetch_commands()
    clear_inputs()
    messagebox.showinfo("Success", "Command added successfully!")

def delete_command():
    selected_item = result_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No command selected!")
        return

    item = result_tree.item(selected_item)
    command_id = item["values"][0]

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM commands WHERE id=?", (command_id,))
    conn.commit()
    conn.close()

    fetch_commands()
    messagebox.showinfo("Deleted", "Command deleted successfully!")

def edit_command():
    selected_item = result_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No command selected!")
        return

    item = result_tree.item(selected_item)
    command_id = item["values"][0]
    
    new_lang = language_entry.get()
    new_cmd = command_entry.get()
    new_desc = description_entry.get()

    if not new_lang or not new_cmd or not new_desc:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE commands SET language = ?, command = ?, description = ? WHERE id = ?",
                   (new_lang, new_cmd, new_desc, command_id))
    conn.commit()
    conn.close()

    fetch_commands()
    clear_inputs()
    messagebox.showinfo("Updated", "Command updated successfully!")

def clear_inputs():
    language_entry.delete(0, tk.END)
    command_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

root = tb.Window(themename="darkly")
root.title("Code Cheat Sheet")
root.geometry("700x500")


style = ttk.Style()
style.configure("Treeview", font=("Arial", 12))  
style.configure("Treeview.Heading", font
=("Arial", 16, "bold")) 
style.configure("Treeview", rowheight=40)

filter_frame = ttk.Frame(root)
filter_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(filter_frame, text="Language:").grid(row=0, column=0, padx=5)
language_var = tk.StringVar()
language_dropdown = ttk.Combobox(filter_frame, textvariable=language_var, state="readonly")
language_dropdown.grid(row=0, column=1, padx=5)
language_dropdown["values"] = ["All", "Python", "Bash", "SQL", "Pentest"]
language_dropdown.current(0)

ttk.Label(filter_frame, text="Search:").grid(row=0, column=2, padx=5)
search_var = tk.StringVar()
search_entry = ttk.Entry(filter_frame, textvariable=search_var)
search_entry.grid(row=0, column=3, padx=5)

search_button = ttk.Button(filter_frame, text="Search", command=fetch_commands)
search_button.grid(row=0, column=4, padx=5)

columns = ("Description", "Command")
result_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    result_tree.heading(col, text=col)
    result_tree.column(col, anchor="w", width=150, stretch=True)

result_tree.pack(padx=10, pady=10, fill="both", expand=True)

entry_frame = ttk.Frame(root)
entry_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(entry_frame, text="Language:").grid(row=0, column=0, padx=5)
language_entry = ttk.Entry(entry_frame)
language_entry.grid(row=0, column=1, padx=5)

ttk.Label(entry_frame, text="Command:").grid(row=0, column=2, padx=5)
command_entry = ttk.Entry(entry_frame)
command_entry.grid(row=0, column=3, padx=5)

ttk.Label(entry_frame, text="Description:").grid(row=0, column=4, padx=5)
description_entry = ttk.Entry(entry_frame)
description_entry.grid(row=0, column=5, padx=5)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Add", command=add_command).pack(side="left", padx=5)
ttk.Button(button_frame, text="Edit", command=edit_command).pack(side="left", padx=5)
ttk.Button(button_frame, text="Delete", command=delete_command).pack(side="left", padx=5)

fetch_commands()

root.mainloop()
