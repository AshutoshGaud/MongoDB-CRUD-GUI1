import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient

# ---- MongoDB Connection ----
client = MongoClient("mongodb://localhost:27017/")
db = client.EmployeeData
collection = db.Employees


# ----------------- Create -----------------
def create_gui(frame):
    def insert():
        eid = entry_id.get()
        name = entry_name.get()
        age = entry_age.get()
        country = entry_country.get()

        if eid and name and age and country:
            collection.insert_one({
                "id": eid,
                "name": name,
                "age": age,
                "country": country
            })
            messagebox.showinfo("Success", "Employee Added!")
        else:
            messagebox.showwarning("Input Error", "Fill all fields")

    tk.Label(frame, text="Employee ID").pack()
    entry_id = tk.Entry(frame); entry_id.pack()

    tk.Label(frame, text="Name").pack()
    entry_name = tk.Entry(frame); entry_name.pack()

    tk.Label(frame, text="Age").pack()
    entry_age = tk.Entry(frame); entry_age.pack()

    tk.Label(frame, text="Country").pack()
    entry_country = tk.Entry(frame); entry_country.pack()

    tk.Button(frame, text="Insert", command=insert, bg="lightgreen").pack(pady=5)


# ----------------- Read -----------------
def read_gui(frame):
    cols = ("ID", "Name", "Age", "Country")
    tree = ttk.Treeview(frame, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        for emp in collection.find():
            tree.insert("", "end", values=(emp["id"], emp["name"], emp["age"], emp["country"]))

    tk.Button(frame, text="Load Data", command=load_data, bg="lightblue").pack(pady=5)


# ----------------- Update -----------------
def update_gui(frame):
    def update():
        name = entry_name.get()
        new_age = entry_age.get()
        new_country = entry_country.get()

        if name and new_age and new_country:
            result = collection.update_one(
                {"name": name},
                {"$set": {"age": new_age, "country": new_country}}
            )
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Record Updated!")
            else:
                messagebox.showwarning("Not Found", "No record found")
        else:
            messagebox.showwarning("Input Error", "Fill all fields")

    tk.Label(frame, text="Name to Update").pack()
    entry_name = tk.Entry(frame); entry_name.pack()

    tk.Label(frame, text="New Age").pack()
    entry_age = tk.Entry(frame); entry_age.pack()

    tk.Label(frame, text="New Country").pack()
    entry_country = tk.Entry(frame); entry_country.pack()

    tk.Button(frame, text="Update", command=update, bg="orange").pack(pady=5)


# ----------------- Delete -----------------
def delete_gui(frame):
    def delete():
        name = entry_name.get()
        if name:
            result = collection.delete_one({"name": name})
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "Record Deleted!")
            else:
                messagebox.showwarning("Not Found", "No record found")
        else:
            messagebox.showwarning("Input Error", "Enter a name")

    tk.Label(frame, text="Name to Delete").pack()
    entry_name = tk.Entry(frame); entry_name.pack()

    tk.Button(frame, text="Delete", command=delete, bg="red").pack(pady=5)


# ----------------- Main GUI -----------------
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

def show_create():
    clear_frame()
    create_gui(frame)

def show_read():
    clear_frame()
    read_gui(frame)

def show_update():
    clear_frame()
    update_gui(frame)

def show_delete():
    clear_frame()
    delete_gui(frame)


root = tk.Tk()
root.title("MongoDB Employee CRUD")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Navigation Buttons
tk.Button(root, text="Create", command=show_create, bg="lightgreen").pack(side="left", padx=5, pady=5)
tk.Button(root, text="Read", command=show_read, bg="lightblue").pack(side="left", padx=5, pady=5)
tk.Button(root, text="Update", command=show_update, bg="orange").pack(side="left", padx=5, pady=5)
tk.Button(root, text="Delete", command=show_delete, bg="red").pack(side="left", padx=5, pady=5)

root.mainloop()
