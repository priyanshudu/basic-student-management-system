from tkinter import *
from tkinter import messagebox
import sqlite3

# Database setup
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS students
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT, rollno TEXT, subject TEXT)''')
con.commit()
con.close()

# ---------------- Functions ---------------- #
def add_student():
    sname = name_var.get()
    sroll = roll_var.get()
    ssubject = subject_var.get()

    if sname == "" or sroll == "" or ssubject == "":
        messagebox.showwarning("Error", "Please fill all fields")
    else:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO students VALUES(NULL,?,?,?)",
                    (sname, sroll, ssubject))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Student Added")

        name_var.set("")
        roll_var.set("")
        subject_var.set("")

def show_students():
    for widget in page2.winfo_children():
        widget.destroy()

    Label(page2, text="All Students").pack()

    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    con.close()

    for row in rows:
        Label(page2, text=f"{row[0]} | {row[1]} | {row[2]} | {row[3]}").pack()

    Button(page2, text="Back", command=lambda: page1.tkraise()).pack()
    Button(page2, text="Delete Student", command=lambda: page3.tkraise()).pack()
    Button(page2, text="Update Student", command=lambda: page4.tkraise()).pack()

def delete_student():
    sid = delete_id_var.get()
    if sid == "":
        messagebox.showwarning("Error", "Enter ID")
    else:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE id=?", (sid,))
        con.commit()
        con.close()
        messagebox.showinfo("Success", f"Student {sid} Deleted")
        delete_id_var.set("")
        show_students()
        page2.tkraise() # Return to show students page

def update_student():
    sid = update_id_var.get()
    newname = update_name_var.get()
    newroll = update_roll_var.get()
    newsub = update_subject_var.get()

    if sid == "" or newname == "" or newroll == "" or newsub == "":
        messagebox.showwarning("Error", "Fill all fields")
    else:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("UPDATE students SET name=?, rollno=?, course=? WHERE id=?",
                    (newname, newroll, newsub, sid))
        con.commit()
        con.close()
        messagebox.showinfo("Success", f"Student {sid} Updated")
        update_id_var.set("")
        update_name_var.set("")
        update_roll_var.set("")
        update_subject_var.set("")
        show_students()
        page2.tkraise()

# ---------------- Main Window ---------------- #
root = Tk()
root.geometry("400x400")
root.title("Student Management")

# Frames
page1 = Frame(root)  # Add
page2 = Frame(root)  # Show
page3 = Frame(root)  # Delete
page4 = Frame(root)  # Update

for frame in (page1, page2, page3, page4):
    frame.grid(row=0, column=0, sticky="nsew")

# -------- Page 1: Add Student -------- #
name_var = StringVar()
roll_var = StringVar()
subject_var = StringVar()

Label(page1, text="Add Student").pack()
Label(page1, text="Name").pack()
Entry(page1, textvariable=name_var).pack()
Label(page1, text="Roll No").pack()
Entry(page1, textvariable=roll_var).pack()
Label(page1, text="Subject").pack()
Entry(page1, textvariable=subject_var).pack()
Button(page1, text="Add", command=add_student).pack()
Button(page1, text="Show Students", command=lambda: (show_students(), page2.tkraise())).pack()
Button(page1, text="Exit", command=root.destroy).pack()

# -------- Page 2: Show Students -------- #
# (content created by show_students)

# -------- Page 3: Delete Student -------- #
delete_id_var = StringVar()
Label(page3, text="Delete Student by ID").pack()
Entry(page3, textvariable=delete_id_var).pack()
Button(page3, text="Delete", command=delete_student).pack()
Button(page3, text="Back", command=lambda: page2.tkraise()).pack()

# -------- Page 4: Update Student -------- #
update_id_var = StringVar()
update_name_var = StringVar()
update_roll_var = StringVar()
update_subject_var = StringVar()

Label(page4, text="Update Student").pack()
Label(page4, text="ID").pack()
Entry(page4, textvariable=update_id_var).pack()
Label(page4, text="New Name").pack()
Entry(page4, textvariable=update_name_var).pack()
Label(page4, text="New Roll No").pack()
Entry(page4, textvariable=update_roll_var).pack()
Label(page4, text="New Subject").pack()
Entry(page4, textvariable=update_subject_var).pack()
Button(page4, text="Update", command=update_student).pack()
Button(page4, text="Back", command=lambda: page2.tkraise()).pack()

# Start on page1
page1.tkraise()

root.mainloop()
