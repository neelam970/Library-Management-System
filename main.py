import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import mysql.connector
from datetime import date

# ------------------ Database Connection ------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="library_db"
)
cursor = conn.cursor()

# ------------------ Main Window ------------------
root = tk.Tk()
root.title("Library Management System")
root.geometry("1200x1000")
root.configure(bg="#f5f5f5")

title = tk.Label(
    root,
    text="Library Management System",
    font=("Segoe UI", 20, "bold"),
    bg="#f5f5f5"
)
title.pack(pady=10)

# ------------------ Book Section ------------------
book_frame = tk.LabelFrame(root, text="Add New Book", font=("Segoe UI", 12, "bold"),
                           bg="#f5f5f5", bd=1, relief="solid")
book_frame.place(x=20, y=70, width=560, height=320)

book_list_frame = tk.LabelFrame(root, text="Book List", font=("Segoe UI", 12, "bold"),
                                bg="#f5f5f5", bd=1, relief="solid")
book_list_frame.place(x=600, y=70, width=560, height=320)

labels = ["Book ID:", "Title:", "Author:", "Publisher:", "Total Copies:", "Image Path:"]
entries = []

def browse_image():
    filepath = filedialog.askopenfilename(
        title="Select Book Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
    )
    if filepath:
        entries[5].delete(0, tk.END)
        entries[5].insert(0, filepath.replace("\\", "/"))

for i, text in enumerate(labels):
    tk.Label(book_frame, text=text, bg="#f5f5f5", font=("Segoe UI", 10)).grid(row=i, column=0, padx=10, pady=6, sticky="w")
    e = tk.Entry(book_frame, width=35)
    e.grid(row=i, column=1, padx=10, pady=6)
    entries.append(e)

tk.Button(book_frame, text="Browse", command=browse_image).grid(row=5, column=2, padx=5)

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

    try:
        cursor.execute(
            "INSERT INTO book (book_id, title, author, publisher, total_copies, image_path) VALUES (%s,%s,%s,%s,%s,%s)",
            (book_id, title_, author, publisher, total_copies, image_path)
        )
        conn.commit()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "Book ID already exists!")
        return

    book_tree.insert("", "end", values=(book_id, title_, author, total_copies))
    messagebox.showinfo("Success", "Book Added Successfully!")
    for e in entries:
        e.delete(0, tk.END)

tk.Button(book_frame, text="Add Book", bg="#43a047", fg="white",
          font=("Segoe UI", 10, "bold"), width=15, command=add_book).grid(row=6, column=0, pady=10)

# ------------------ Book List ------------------
book_tree = ttk.Treeview(book_list_frame, columns=("id", "title", "author", "total"), show="headings", height=12)
book_tree.heading("id", text="ID")
book_tree.heading("title", text="Title")
book_tree.heading("author", text="Author")
book_tree.heading("total", text="Total Copies")
book_tree.column("id", width=50)
book_tree.column("title", width=180)
book_tree.column("author", width=150)
book_tree.column("total", width=100)
book_tree.pack(fill="both", padx=10, pady=10)

# ------------------ Member Section ------------------
member_frame = tk.LabelFrame(root, text="Add New Member", font=("Segoe UI", 12, "bold"),
                             bg="#f5f5f5", bd=1, relief="solid")
member_frame.place(x=20, y=410, width=560, height=220)

member_list_frame = tk.LabelFrame(root, text="Member List", font=("Segoe UI", 12, "bold"),
                                  bg="#f5f5f5", bd=1, relief="solid")
member_list_frame.place(x=600, y=410, width=560, height=220)

m_labels = ["Member ID:", "Name:", "Email:", "Phone_no:"]
m_entries = []

for i, text in enumerate(m_labels):
    tk.Label(member_frame, text=text, bg="#f5f5f5", font=("Segoe UI", 10)).grid(row=i, column=0, padx=10, pady=6, sticky="w")
    e = tk.Entry(member_frame, width=35)
    e.grid(row=i, column=1, padx=10, pady=6)
    m_entries.append(e)

def add_member():
    member_id = m_entries[0].get()
    name = m_entries[1].get()
    email = m_entries[2].get()
    phone_no = m_entries[3].get()

    if member_id == "" or name == "":
        messagebox.showerror("Error", "Member ID and Name are required!")
        return

    try:
        cursor.execute(
            "INSERT INTO member (member_id, name, email, phone_no) VALUES (%s,%s,%s,%s)",
            (member_id, name, email, phone_no)
        )
        conn.commit()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "Member ID already exists!")
        return

    member_tree.insert("", "end", values=(member_id, name, email))
    messagebox.showinfo("Success", "Member Added Successfully!")
    for e in m_entries:
        e.delete(0, tk.END)

tk.Button(member_frame, text="Add Member", bg="#43a047", fg="white",
          font=("Segoe UI", 10, "bold"), width=15, command=add_member).grid(row=4, column=0, pady=10)

# ------------------ Member List ------------------
member_tree = ttk.Treeview(member_list_frame, columns=("id", "name", "email"), show="headings", height=12)
member_tree.heading("id", text="ID")
member_tree.heading("name", text="Name")
member_tree.heading("email", text="Email")
member_tree.column("id", width=60)
member_tree.column("name", width=180)
member_tree.column("email", width=250)
member_tree.pack(fill="both", padx=10, pady=10)

# ------------------ Transactions Section ------------------
transaction_frame = tk.LabelFrame(root, text="Book Transactions", font=("Segoe UI", 12, "bold"),
                                  bg="#f5f5f5", bd=1, relief="solid")
transaction_frame.place(x=20, y=650, width=1140, height=320)

# Issue / Return Frames
issue_frame = tk.LabelFrame(transaction_frame, text="Issue Book", bg="#f5f5f5", bd=1, relief="solid")
issue_frame.place(x=10, y=5, width=550, height=70)

return_frame = tk.LabelFrame(transaction_frame, text="Return Book", bg="#f5f5f5", bd=1, relief="solid")
return_frame.place(x=580, y=5, width=550, height=70)

tk.Label(issue_frame, text="Book ID:", bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=10)
tk.Label(issue_frame, text="Member ID:", bg="#f5f5f5").grid(row=0, column=2, padx=10)
issue_entries = [tk.Entry(issue_frame, width=15), tk.Entry(issue_frame, width=15)]
issue_entries[0].grid(row=0, column=1)
issue_entries[1].grid(row=0, column=3)

tk.Label(return_frame, text="Book ID:", bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=10)
tk.Label(return_frame, text="Member ID:", bg="#f5f5f5").grid(row=0, column=2, padx=10)
return_entries = [tk.Entry(return_frame, width=15), tk.Entry(return_frame, width=15)]
return_entries[0].grid(row=0, column=1)
return_entries[1].grid(row=0, column=3)

# Issue Log Table
issue_tree_frame = tk.Frame(transaction_frame)
issue_tree_frame.place(x=10, y=90, width=1120, height=220)

issue_tree = ttk.Treeview(issue_tree_frame, columns=("book_id", "member_id", "issue_date", "return_date"),
                          show="headings")
issue_tree.heading("book_id", text="Book ID")
issue_tree.heading("member_id", text="Member ID")
issue_tree.heading("issue_date", text="Issue Date")
issue_tree.heading("return_date", text="Return Date")
issue_tree.column("book_id", width=100)
issue_tree.column("member_id", width=120)
issue_tree.column("issue_date", width=150)
issue_tree.column("return_date", width=150)
issue_tree.pack(fill="both", expand=True)

# ------------------ Functions for Issue / Return ------------------
def load_issue_data():
    for row in issue_tree.get_children():
        issue_tree.delete(row)
    cursor.execute("SELECT book_id, member_id, issue_date, return_date FROM issue_log")
    for row in cursor.fetchall():
        issue_tree.insert("", "end", values=row)

def issue_book():
    book_id = issue_entries[0].get()
    member_id = issue_entries[1].get()

    if book_id == "" or member_id == "":
        messagebox.showerror("Error", "Book ID and Member ID are required!")
        return

    try:
        cursor.execute(
            "INSERT INTO issue_log (book_id, member_id, issue_date, return_date) VALUES (%s,%s,%s,NULL)",
            (book_id, member_id, date.today())
        )
        conn.commit()
        messagebox.showinfo("Success", "Book Issued Successfully!")
    except mysql.connector.errors.IntegrityError as e:
        messagebox.showerror("Error", f"Error issuing book: {str(e)}")

    for e in issue_entries:
        e.delete(0, tk.END)
    load_issue_data()

def return_book():
    book_id = return_entries[0].get()
    member_id = return_entries[1].get()

    if book_id == "" or member_id == "":
        messagebox.showerror("Error", "Book ID and Member ID are required!")
        return

    try:
        cursor.execute(
            "UPDATE issue_log SET return_date=%s WHERE book_id=%s AND member_id=%s AND return_date IS NULL",
            (date.today(), book_id, member_id)
        )
        conn.commit()
        messagebox.showinfo("Success", "Book Returned Successfully!")
    except mysql.connector.errors.IntegrityError as e:
        messagebox.showerror("Error", f"Error returning book: {str(e)}")

    for e in return_entries:
        e.delete(0, tk.END)
    load_issue_data()

tk.Button(issue_frame, text="Issue Book", bg="#ef6c00", fg="white", font=("Segoe UI", 10, "bold"), width=12,
          command=issue_book).grid(row=0, column=4, padx=15)

tk.Button(return_frame, text="Return Book", bg="#c62828", fg="white", font=("Segoe UI", 10, "bold"), width=12,
          command=return_book).grid(row=0, column=4, padx=15)

# ------------------ Load data on start ------------------
def load_books():
    book_tree.delete(*book_tree.get_children())
    cursor.execute("SELECT book_id, title, author, total_copies FROM book")
    for row in cursor.fetchall():
        book_tree.insert("", "end", values=row)

def load_members():
    member_tree.delete(*member_tree.get_children())
    cursor.execute("SELECT member_id, name, email FROM member")
    for row in cursor.fetchall():
        member_tree.insert("", "end", values=row)

load_books()
load_members()
load_issue_data()

# ------------------ Run App ------------------
root.mainloop()




