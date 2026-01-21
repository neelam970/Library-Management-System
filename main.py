import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import mysql.connector
import os

# ---------- Database Connection ----------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="library_db"
)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    publisher VARCHAR(100),
    total_copies INT,
    image_path VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
)
""")
conn.commit()

# ---------- Main Window ----------
root = tk.Tk()
root.title("Library Management System")
root.geometry("1200x800")
root.configure(bg="#f5f5f5")

title = tk.Label(
    root,
    text="Library Management System",
    font=("Segoe UI", 20, "bold"),
    bg="#f5f5f5"
)
title.pack(pady=10)

# ---------- Frames ----------
book_frame = tk.LabelFrame(root, text="Add New Book", font=("Segoe UI", 12, "bold"),
                           bg="#f5f5f5", bd=1, relief="solid")
book_frame.place(x=20, y=70, width=560, height=300)

book_list_frame = tk.LabelFrame(root, text="Book List", font=("Segoe UI", 12, "bold"),
                                bg="#f5f5f5", bd=1, relief="solid")
book_list_frame.place(x=600, y=70, width=560, height=300)

member_frame = tk.LabelFrame(root, text="Add New Member", font=("Segoe UI", 12, "bold"),
                             bg="#f5f5f5", bd=1, relief="solid")
member_frame.place(x=20, y=390, width=560, height=260)

member_list_frame = tk.LabelFrame(root, text="Member List", font=("Segoe UI", 12, "bold"),
                                  bg="#f5f5f5", bd=1, relief="solid")
member_list_frame.place(x=600, y=390, width=560, height=260)

transaction_frame = tk.LabelFrame(root, text="Book Transactions", font=("Segoe UI", 12, "bold"),
                                  bg="#f5f5f5", bd=1, relief="solid")
transaction_frame.place(x=20, y=670, width=1140, height=110)

# ---------- Treeview Style ----------
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#d3d3d3",
                foreground="black",
                rowheight=25,
                fieldbackground="#d3d3d3",
                font=("Segoe UI", 10))
style.map('Treeview', background=[('selected', '#347083')])
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e0e0e0")

# ---------- Functions ----------
def browse_image():
    filepath = filedialog.askopenfilename(
        title="Select Book Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
    )
    if filepath:
        # Convert Windows backslashes to forward slashes
        filepath = filepath.replace("\\", "/")
        entries[5].delete(0, tk.END)
        entries[5].insert(0, filepath)

def add_book():
    book_id = entries[0].get()
    title_ = entries[1].get()
    author = entries[2].get()
    publisher = entries[3].get()
    total_copies = entries[4].get()
    image_path = entries[5].get()

    if book_id == "" or title_ == "" or author == "":
        messagebox.showerror("Error", "Book ID, Title, and Author are required!")
        return

    # Insert into database
    try:
        cursor.execute(
            "INSERT INTO books (id, title, author, publisher, total_copies, image_path) VALUES (%s,%s,%s,%s,%s,%s)",
            (book_id, title_, author, publisher, total_copies, image_path)
        )
        conn.commit()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "Book ID already exists!")
        return

    # Insert into Treeview with striped rows
    count = len(book_tree.get_children())
    tag = 'evenrow' if count % 2 == 0 else 'oddrow'
    book_tree.insert("", "end", values=(book_id, title_, author, total_copies), tags=(tag,))
    book_tree.tag_configure('evenrow', background='#d3d3d3')
    book_tree.tag_configure('oddrow', background='#c0c0c0')

    messagebox.showinfo("Success", "Book Added Successfully!")

    # Clear entries and image
    for e in entries:
        e.delete(0, tk.END)
    book_image_label.config(image='')
    book_image_label.image = None

def add_member():
    member_id = m_entries[0].get()
    name = m_entries[1].get()
    email = m_entries[2].get()
    phone = m_entries[3].get()

    if member_id == "" or name == "":
        messagebox.showerror("Error", "Member ID and Name are required!")
        return

    # Insert into database
    try:
        cursor.execute(
            "INSERT INTO members (id, name, email, phone) VALUES (%s,%s,%s,%s)",
            (member_id, name, email, phone)
        )
        conn.commit()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "Member ID already exists!")
        return

    # Insert into Treeview with striped rows
    count = len(member_tree.get_children())
    tag = 'evenrow' if count % 2 == 0 else 'oddrow'
    member_tree.insert("", "end", values=(member_id, name, email), tags=(tag,))
    member_tree.tag_configure('evenrow', background='#d3d3d3')
    member_tree.tag_configure('oddrow', background='#c0c0c0')

    messagebox.showinfo("Success", "Member Added Successfully!")

    for e in m_entries:
        e.delete(0, tk.END)

def issue_book():
    messagebox.showinfo("Success", "Book Issued Successfully!")

def return_book():
    messagebox.showinfo("Success", "Book Returned Successfully!")

def show_book_image(event):
    selected = book_tree.focus()
    if selected:
        values = book_tree.item(selected, 'values')
        book_id = values[0]

        cursor.execute("SELECT image_path FROM books WHERE id=%s", (book_id,))
        result = cursor.fetchone()

        if result and result[0] and os.path.exists(result[0]):
            img_path = result[0]
            try:
                img = Image.open(img_path)
                img = img.resize((120, 150))  # Resize image to fit label
                photo = ImageTk.PhotoImage(img)
                book_image_label.config(image=photo)
                book_image_label.image = photo  # Keep reference
            except Exception as e:
                book_image_label.config(image='')
                book_image_label.image = None
        else:
            # Show placeholder if image missing
            img = Image.new('RGB', (120,150), color='gray')
            photo = ImageTk.PhotoImage(img)
            book_image_label.config(image=photo)
            book_image_label.image = photo

# ---------- Book Section ----------
labels = ["Book ID:", "Title:", "Author:", "Publisher:", "Total Copies:", "Image Path:"]
entries = []

for i, text in enumerate(labels):
    tk.Label(book_frame, text=text, bg="#f5f5f5", font=("Segoe UI", 10)).grid(
        row=i, column=0, padx=10, pady=6, sticky="w"
    )
    e = tk.Entry(book_frame, width=35)
    e.grid(row=i, column=1, padx=10, pady=6)
    entries.append(e)

tk.Button(book_frame, text="Browse", command=browse_image).grid(row=5, column=2, padx=5)

tk.Button(
    book_frame, text="Add Book", bg="#43a047", fg="white",
    font=("Segoe UI", 10, "bold"), width=15, command=add_book
).grid(row=6, column=0, pady=15)

# ---------- Book List ----------
book_tree = ttk.Treeview(book_list_frame, columns=("id", "title", "author", "avail"), show="headings", height=6)
book_tree.heading("id", text="ID")
book_tree.heading("title", text="Title")
book_tree.heading("author", text="Author")
book_tree.heading("avail", text="Total Copies")
book_tree.column("id", width=50)
book_tree.column("title", width=180)
book_tree.column("author", width=150)
book_tree.column("avail", width=100)
book_tree.pack(side="left", fill="x", padx=10, pady=10)
book_tree.bind("<<TreeviewSelect>>", show_book_image)

book_image_label = tk.Label(book_list_frame, bg="#f5f5f5")
book_image_label.pack(side="right", padx=10, pady=10)

# ---------- Member Section ----------
m_labels = ["Member ID:", "Name:", "Email:", "Phone:"]
m_entries = []

for i, text in enumerate(m_labels):
    tk.Label(member_frame, text=text, bg="#f5f5f5", font=("Segoe UI", 10)).grid(
        row=i, column=0, padx=10, pady=6, sticky="w"
    )
    e = tk.Entry(member_frame, width=35)
    e.grid(row=i, column=1, padx=10, pady=6)
    m_entries.append(e)

tk.Button(
    member_frame, text="Add Member", bg="#43a047", fg="white",
    font=("Segoe UI", 10, "bold"), width=15, command=add_member
).grid(row=4, column=0, pady=15)

# ---------- Member List ----------
member_tree = ttk.Treeview(member_list_frame, columns=("id", "name", "email"), show="headings", height=6)
member_tree.heading("id", text="ID")
member_tree.heading("name", text="Name")
member_tree.heading("email", text="Email")
member_tree.column("id", width=60)
member_tree.column("name", width=180)
member_tree.column("email", width=250)
member_tree.pack(fill="x", padx=10, pady=10)

# ---------- Transactions ----------
issue_frame = tk.LabelFrame(transaction_frame, text="Issue Book", bg="#f5f5f5", bd=1, relief="solid")
issue_frame.place(x=10, y=5, width=550, height=80)

return_frame = tk.LabelFrame(transaction_frame, text="Return Book", bg="#f5f5f5", bd=1, relief="solid")
return_frame.place(x=580, y=5, width=550, height=80)

tk.Label(issue_frame, text="Book ID:", bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(issue_frame, width=15).grid(row=0, column=1)
tk.Label(issue_frame, text="Member ID:", bg="#f5f5f5").grid(row=0, column=2, padx=10)
tk.Entry(issue_frame, width=15).grid(row=0, column=3)
tk.Button(
    issue_frame, text="Issue Book", bg="#ef6c00", fg="white",
    font=("Segoe UI", 10, "bold"), width=12, command=issue_book
).grid(row=0, column=4, padx=15)

tk.Label(return_frame, text="Book ID:", bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(return_frame, width=15).grid(row=0, column=1)
tk.Label(return_frame, text="Member ID:", bg="#f5f5f5").grid(row=0, column=2, padx=10)
tk.Entry(return_frame, width=15).grid(row=0, column=3)
tk.Button(
    return_frame, text="Return Book", bg="#c62828", fg="white",
    font=("Segoe UI", 10, "bold"), width=12, command=return_book
).grid(row=0, column=4, padx=15)

root.mainloop()




