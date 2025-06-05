import tkinter as tk
from tkinter import messagebox
import random

tasks = []
daily_reflections = [
    "מה גרם לך לחייך היום?",
    "על מה אתה מרגיש גאווה השבוע?",
    "מה הייתה אתגר שלך היום ואיך התמודדת איתו?",
    "איך עזרת למישהו היום?",
    "על מה אתה מודה היום?"
]

# פונקציה להוספת משימה
def add_task():
    task = task_entry.get()
    if task:
        tasks.append({"task": task, "done": False})
        update_task_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("שגיאה", "אנא הזן תיאור משימה")

# עדכון רשימת משימות
def update_task_list():
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔️" if task["done"] else "⬜"
        listbox.insert(tk.END, f"{task['task']} {status}")

# סימון משימה כבוצעה
def mark_done():
    index = listbox.curselection()
    if index:
        i = index[0]
        tasks[i]["done"] = True
        update_task_list()
        messagebox.showinfo("מעולה!", "🎉 כל הכבוד! סיימת משימה.")
    else:
        messagebox.showwarning("שגיאה", "בחר/י משימה מתוך הרשימה")

# הצגת שאלת השראה
def show_reflection():
    reflection = random.choice(daily_reflections)
    messagebox.showinfo("שאלת השראה יומית", f"💭 {reflection}")

# GUI ראשי
app = tk.Tk()
app.title("מנהל חזרה לשגרה")
app.geometry("500x500")

tk.Label(app, text="הזן משימה חדשה:").pack(pady=5)
task_entry = tk.Entry(app, width=40)
task_entry.pack(pady=5)

tk.Button(app, text="➕ הוסף משימה", command=add_task).pack(pady=5)
tk.Button(app, text="✔️ סמן כבוצעה", command=mark_done).pack(pady=5)
tk.Button(app, text="💭 שאלת השראה יומית", command=show_reflection).pack(pady=5)

tk.Label(app, text="📋 רשימת משימות:").pack(pady=10)
listbox = tk.Listbox(app, width=50, height=10)
listbox.pack(pady=10)

tk.Button(app, text="🚪 יציאה", command=app.quit).pack(pady=10)

app.mainloop()