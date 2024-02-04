import tkinter as tk
from tkinter import ttk
import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database= "pythonwork_014"
)

columns = ("StudentID", "StudentName", "StudentLastName", "Age")
cursor = database.cursor()

insert_row = "StudentName, StudentLastName, Age"

def insert_command():
    EntryName = StudentName_Entry.get()
    EntryLastName = StudentLastName_Entry.get()
    EntryAge = Age_Entry.get()

    Query = f"INSERT INTO studentinfo ({insert_row}) VALUES (%s, %s, %s)"
    cursor.execute(Query, (EntryName, EntryLastName, EntryAge))
    
    database.commit()
    update_treeview()

def delete_command():
    selection = view.selection()
    if selection:
        item_id = selection[0]
        cursor.execute("DELETE FROM studentinfo WHERE StudentID = %s", (view.item(item_id, 'values')[0],))
        database.commit()
        update_treeview()

def edit_command():
    selection = view.selection()
    if selection:
        item_id = selection[0]
        # Retrieve existing data
        existing_data = view.item(item_id, 'values')
        
        # Clear entry widgets
        clear_entry_widgets()

        # Populate entry widgets with existing data for editing
        StudentName_Entry.insert(0, existing_data[1])
        StudentLastName_Entry.insert(0, existing_data[2])
        Age_Entry.insert(0, existing_data[3])

def update_command():
    selection = view.selection()
    if selection:
        item_id = selection[0]
        EntryName = StudentName_Entry.get()
        EntryLastName = StudentLastName_Entry.get()
        EntryAge = Age_Entry.get()

        # Update the database with new data
        update_query = "UPDATE studentinfo SET StudentName = %s, StudentLastName = %s, Age = %s WHERE StudentID = %s"
        cursor.execute(update_query, (EntryName, EntryLastName, EntryAge, view.item(item_id, 'values')[0]))
        
        database.commit()
        clear_entry_widgets()
        update_treeview()

def clear_entry_widgets():
    StudentName_Entry.delete(0, tk.END)
    StudentLastName_Entry.delete(0, tk.END)
    Age_Entry.delete(0, tk.END)

def update_treeview():
    cursor.execute("SELECT * FROM studentinfo")
    records = cursor.fetchall()

    for deldata in view.get_children():
        view.delete(deldata)

    for i, datarow in enumerate(records):
        tags = ('evenrow', 'oddrow')[i % 2]
        view.insert('', 'end', values=datarow, tags=tags)





# Make tkinter
root = tk.Tk()

# LabelName
StudentName_label = ttk.Label(root, text="กรอกชื่อ :")
StudentName_label.grid(row=0, column=0, padx=5, pady=5)

# MakeEntryForname
StudentName_Entry = ttk.Entry(root)
StudentName_Entry.grid(row=0, column=1, padx=5, pady=5)

# LabelLastName
StudentLastName_label = ttk.Label(root, text="กรอกนามสกุล :")
StudentLastName_label.grid(row=1, column=0, padx=5, pady=5)

# MakeEntryForLastname
StudentLastName_Entry = ttk.Entry(root)
StudentLastName_Entry.grid(row=1, column=1, padx=5, pady=5)

# LabelAge
Age_label = ttk.Label(root, text="อายุ :")
Age_label.grid(row=2, column=0, padx=5, pady=5)

# Entry Age
Age_Entry = ttk.Entry(root)
Age_Entry.grid(row=2, column=1, padx=5, pady=5)

# Insert Button
Insert_button = ttk.Button(root, text="Insert", command=insert_command)
Insert_button.grid(row=3, column=0, pady=10)

delete_button = ttk.Button(root, text="Delete", command=delete_command)
delete_button.grid(row=3, column=1, pady=10)

# Edit Button
edit_button = ttk.Button(root, text="Edit", command=edit_command)
edit_button.grid(row=3, column=2, pady=10)

# Update Button
update_button = ttk.Button(root, text="Update", command=update_command)
update_button.grid(row=3, column=3, pady=10)

# Show Data
view = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    view.heading(col, text=col, anchor="center")

# Configure tags for alternating row colors
view.tag_configure('evenrow', background='#f0f0f0')  # Light gray
view.tag_configure('oddrow', background='#e0e0e0')   # Slightly darker gray

view.grid(row=4, column=0, columnspan=4, pady=10)

# Update Data
update_treeview()


# Start the Tkinter main loop
if __name__ == "__main__":
    root.mainloop()

# Close resources using try...finally
try:
    cursor.close()
    database.close()
    print("Database has closed successfully")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    print("การเชื่อมต่อมีปัญหา")
