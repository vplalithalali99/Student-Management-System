import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
import sqlite3
import csv
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()
conn.close()
print("Database Created Successfully!")
def add_student_db(name, age, course):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )
    conn.commit()
    conn.close()
def view_students_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return data
def sort_students_db(order):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    query = f"""
    SELECT * FROM students
    ORDER BY age {order}
    """
    cursor.execute(query)
    students = cursor.fetchall()
    conn.close()
    return students
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    if (
        not name
        or not age
        or course == "Select Course"
    ):
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please fill all fields!")
        return
    if not age.isdigit():
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Age must be a number!")
        return
    if student_exists(name):
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Student already exists!")
        return
    add_student_db(name, age, course)
    refresh_table()
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Student Added Successfully!")
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.set("Select Course")
def search_course_db(course):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE course = ?",
        (course,)
    )
    students = cursor.fetchall()
    conn.close()
    return students
def search_student_db(name):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE name = ?",
        (name,)
    )
    student = cursor.fetchone()
    conn.close()
    return student
def live_search(event):
    keyword = name_entry.get()

    if keyword == "":
        refresh_table()
        return
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        (f"%{keyword}%",)
    )
    students = cursor.fetchall()
    conn.close()
    for row in tree.get_children():
        tree.delete(row)
    for student in students:
        tree.insert("", tk.END, values=student)
def view_students():
    students = view_students_db()
    output = ""
    for student in students:
        output += f"ID: {student[0]}\n"
        output += f"Name: {student[1]}\n"
        output += f"Age: {student[2]}\n"
        output += f"Course: {student[3]}\n"
        output += "-------------------\n"
    if output == "":
        output = "No students found"
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)
def sort_students(order):
    students = sort_students_db(order)
    for row in tree.get_children():
        tree.delete(row)
    for student in students:
        tree.insert("", tk.END, values=student)
    result_text.delete("1.0", tk.END)
    if order == "ASC":
        result_text.insert(
            tk.END,
            "Students sorted by age (Low → High)"
        )
    else:
        result_text.insert(
            tk.END,
            "Students sorted by age (High → Low)"
        )
def search_course():
    course = course_entry.get()
    if course == "Select Course":
        result_text.delete("1.0", tk.END)
        result_text.insert(
            tk.END,
            "Enter course name"
        )
        return
    students = search_course_db(course)
    if students:
        output = ""
        for student in students:
            output += (
                f"ID: {student[0]}\n"
                f"Name: {student[1]}\n"
                f"Age: {student[2]}\n"
                f"Course: {student[3]}\n"
                "-----------------\n"
            )
    else:
        output = "No students found"
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)
def search_student():
    name = name_entry.get()
    if not name:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Enter student name")
        return
    student = search_student_db(name)
    if student:
        output = (
            f"ID: {student[0]}\n"
            f"Name: {student[1]}\n"
            f"Age: {student[2]}\n"
            f"Course: {student[3]}"
        )
    else:
        output = "Student Not Found"
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)
def update_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    if not age.isdigit():
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Age must be a number!")
        return
    updated = update_student_db(
        name,
        int(age),
        course
    )
    result_text.delete("1.0", tk.END)
    if updated > 0:
        refresh_table()

        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        course_entry.set("Select Course")

        result_text.insert(
            tk.END,
            "Student Updated Successfully!"
        )
    else:
        result_text.insert(
            tk.END,
            "Student Not Found"
        )
def delete_student_db(name):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM students WHERE name = ?",
        (name,)
    )
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows
def update_student_db(name, age, course):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE students
        SET age = ?, course = ?
        WHERE name = ?
        """,
        (age, course, name)
    )
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    return updated_rows
def delete_student():
    name = name_entry.get()
    if not name:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Enter student name")
        return
    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete {name}?"
    )
    if not confirm:
        return
    deleted = delete_student_db(name)
    result_text.delete("1.0", tk.END)
    if deleted > 0:
        refresh_table()
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        course_entry.set("Select Course")
        result_text.insert(
            tk.END,
            "Student Deleted Successfully!"
        )
    else:
        result_text.insert(
            tk.END,
            "Student Not Found"
        )
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    students = view_students_db()
    for student in students:
        tree.insert("", tk.END, values=student)
    count_label.config(
        text=f"Total Students: {get_student_count()}"
    )
def select_student(event):
    selected = tree.focus()
    values = tree.item(selected, "values")

    if values:
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)

        name_entry.insert(0, values[1])
        age_entry.insert(0, values[2])

        course_entry.set(values[3])
def student_exists(name):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE name = ?",
        (name,)
    )
    student = cursor.fetchone()
    conn.close()
    return student
def get_student_count():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    conn.close()
    return count
def get_statistics():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(age) FROM students")
    avg_age = cursor.fetchone()[0]
    cursor.execute(
        "SELECT name, age FROM students ORDER BY age DESC LIMIT 1"
    )
    oldest = cursor.fetchone()
    cursor.execute(
        "SELECT name, age FROM students ORDER BY age ASC LIMIT 1"
    )
    youngest = cursor.fetchone()
    conn.close()
    return total, avg_age, oldest, youngest
def export_csv():
    students = view_students_db()
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Course"])
        writer.writerows(students)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Students exported to students.csv")
def show_report():
    total, avg_age, oldest, youngest = get_statistics()
    avg_age = avg_age if avg_age else 0
    if total == 0:
        output = "No students available"
    else:
        output = (
            f"Total Students : {total}\n\n"
            f"Average Age    : {avg_age:.2f}\n\n"
            f"Oldest Student : "
            f"{oldest[0]} ({oldest[1]} years)\n\n"
            f"Youngest Student : "
            f"{youngest[0]} ({youngest[1]} years)"
        )
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)
def export_pdf():
    total, avg_age, oldest, youngest = get_statistics()
    pdf = canvas.Canvas("student_report.pdf")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(
        180,
        800,
        "Student Report"
    )
    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        740,
        f"Total Students: {total}"
    )
    avg_age = avg_age if avg_age else 0

    pdf.drawString(
        50,
        710,
        f"Average Age: {avg_age:.2f}"
    )      
    students = view_students_db()
    y = 600
    for student in students:
        pdf.drawString(
            50,
            y,
            f"{student[0]} | {student[1]} | {student[2]} | {student[3]}"
        )
        y -= 20
    if oldest:
        pdf.drawString(
            50,
            680,
            f"Oldest Student: {oldest[0]} ({oldest[1]})"
        )
    if youngest:
        pdf.drawString(
            50,
            650,
            f"Youngest Student: {youngest[0]} ({youngest[1]})"
        )
    pdf.save()
    result_text.delete("1.0", tk.END)
    result_text.insert(
        tk.END,
        "PDF Report exported as student_report.pdf"
    )
def course_statistics():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT course, COUNT(*)
    FROM students
    GROUP BY course
    """)
    data = cursor.fetchall()
    conn.close()
    output = ""
    for course, count in data:
        output += f"{course} : {count}\n"
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.set("Select Course")
    result_text.delete("1.0", tk.END)
# WINDOW
window = tk.Tk()
window.title("Student Management System")
window.geometry("1300x700")
top_frame = tk.Frame(window)
top_frame.pack(pady=10)
button_frame = tk.Frame(window)
button_frame.pack(pady=10)
table_frame = tk.Frame(window)
table_frame.pack(pady=10)
name_label = tk.Label(top_frame, text="Enter Name")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(top_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)
name_entry.bind("<KeyRelease>", live_search)
age_label = tk.Label(top_frame, text="Enter Age")
age_label.grid(row=1, column=0, padx=5, pady=5)
age_entry = tk.Entry(top_frame)
age_entry.grid(row=1, column=1, padx=5, pady=5)
course_label = tk.Label(top_frame, text="Enter Course")
course_label.grid(row=2, column=0, padx=5, pady=5)
course_entry = ttk.Combobox(
    top_frame,
    values=[
        "CSE",
        "AIML",
        "PYTHON",
        "DS",
        "JAVA"
    ],
    state="readonly"
)
course_entry.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)
course_entry.set("Select Course")
count_label = tk.Label(
    window,
    text="Total Students: 0",
    font=("Arial", 12, "bold")
)
count_label.pack(pady=5)
add_button = tk.Button(
    button_frame,
    text="Add Student",
    command=add_student
)
add_button.grid(row=0, column=0, padx=5)

view_button = tk.Button(
    button_frame,
    text="View Students",
    command=view_students
)
view_button.grid(row=0, column=1, padx=5)

search_button = tk.Button(
    button_frame,
    text="Search Student",
    command=search_student
)
search_button.grid(row=0, column=2, padx=5)

delete_button = tk.Button(
    button_frame,
    text="Delete Student",
    command=delete_student
)
delete_button.grid(row=0, column=3, padx=5)

update_button = tk.Button(
    button_frame,
    text="Update Student",
    command=update_student
)
update_button.grid(row=0, column=4, padx=5)

export_button = tk.Button(
    button_frame,
    text="Export CSV",
    command=export_csv
)
clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields
)

clear_button.grid(row=0, column=6, padx=5)
course_search_button = tk.Button(
    button_frame,
    text="Search Course",
    command=search_course
)
course_search_button.grid(
    row=0,
    column=7,
    padx=5
)
report_button = tk.Button(
    button_frame,
    text="Report",
    command=show_report
)

report_button.grid(
    row=0,
    column=10,
    padx=5
)
export_button.grid(row=0, column=5, padx=5)
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical"
)
sort_asc_button = tk.Button(
    button_frame,
    text="Age ↑",
    command=lambda: sort_students("ASC")
)

sort_asc_button.grid(
    row=0,
    column=9,
    padx=5
)
sort_desc_button = tk.Button(
    button_frame,
    text="Age ↓",
    command=lambda: sort_students("DESC")
)

sort_desc_button.grid(
    row=0,
    column=8,
    padx=5
)
pdf_button = tk.Button(
    button_frame,
    text="Export PDF",
    command=export_pdf
)

pdf_button.grid(
    row=0,
    column=11,
    padx=5
)
course_stats_btn = tk.Button(
    button_frame,
    text="Course Stats",
    command=course_statistics
)

course_stats_btn.grid(row=0, column=12)
tree = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Age", "Course"),
    show="headings",
    yscrollcommand=scrollbar.set,
    height=10
)
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")

tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Age", width=80)
tree.column("Course", width=150)

scrollbar.config(command=tree.yview)

tree.pack(side="left")
scrollbar.pack(side="right", fill="y")
x_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="horizontal"
)
tree.configure(
    xscrollcommand=x_scrollbar.set
)
x_scrollbar.config(
    command=tree.xview
)
x_scrollbar.pack(
    side="bottom",
    fill="x"
)
#result box
result_text = tk.Text(window, height=10, width=40)
result_text.pack(pady=10)
tree.bind("<<TreeviewSelect>>", select_student)
#run window
refresh_table()
top_frame.configure(bg="#2b2b2b")
button_frame.configure(bg="#2b2b2b")
table_frame.configure(bg="#2b2b2b")

count_label.configure(
    bg="#2b2b2b",
    fg="white"
)
window.configure(bg="#2b2b2b")
result_text.configure(
    bg="#1e1e1e",
    fg="white"
)
window.mainloop()
