import tkinter as tk
import datetime
from tkinter import PhotoImage, messagebox
import random
import sys

tasks = []

# שאלות השראה
daily_reflections = [
    "מה גרם לך לחייך היום?",
    "על מה אתה מרגיש גאווה השבוע?",
    "מה הייתה אתגר שלך היום ואיך התמודדת איתו?",
    "איך עזרת למישהו היום?",
    "על מה אתה מודה היום?"
]

window = tk.Tk()


# פונקציה להוספת משימה
def add_task(task_entry, time_entry, listbox):
    task = task_entry.get()
    time = time_entry.get()
    if task and time:
        tasks.append({"task": task, "time": time, "done": False})
        update_task_list(listbox)
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("שגיאה", "אנא הזן גם תיאור משימה וגם שעה")


# עדכון רשימת משימות
def update_task_list(listbox):
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔️" if task["done"] else "⬜"
        listbox.insert(tk.END, f"{task['task']} ({task['time']}) {status}")


# סימון משימה כבוצעה
def mark_done(listbox):
    index = listbox.curselection()
    if index:
        i = index[0]
        tasks[i]["done"] = True
        update_task_list(listbox)
        messagebox.showinfo("מעולה!", "🎉 כל הכבוד! סיימת משימה.")
    else:
        messagebox.showwarning("שגיאה", "בחר/י משימה מתוך הרשימה")


# שאלת השראה
def show_reflection():
    reflection = random.choice(daily_reflections)
    messagebox.showinfo("שאלת השראה יומית", f"💭 {reflection}")


# בדיקה של זמני משימות
def check_tasks_for_alerts():
    now = datetime.datetime.now().strftime("%H:%M")
    for task in tasks:
        if not task["done"] and task["time"] == now:
            messagebox.showinfo("תזכורת!", f"המשימה \"{task['task']}\" אמורה להתחיל עכשיו!")
            task["done"] = True
    window.after(30000, check_tasks_for_alerts)


# סגירת האפליקציה לגמרי
def exit_app():
    window.destroy()
    sys.exit()


# פתיחת חלון משימות
def open_new_window():
    name = name_entry.get()
    age = age_entry.get()

    new_window = tk.Toplevel(window)
    new_window.title("מילוי משימות")
    new_window.geometry("700x500")
    new_window.config(bg="#0d6d28")

    label_style = {"font": ("Segoe UI", 16), "bg": "#0d6d28", "fg": "white"}
    entry_style = {"font": ("Segoe UI", 14)}

    tk.Label(new_window, text=f"{name} מה איתך?", font=("Segoe UI", 24, "bold"), bg="#0d6d28", fg="white").pack(pady=10)

    tk.Label(new_window, text="הזן משימה חדשה:", **label_style).pack()
    task_entry = tk.Entry(new_window, width=40, **entry_style)
    task_entry.pack(pady=5)

    tk.Label(new_window, text="הזן שעה למשימה (בפורמט HH:MM):", **label_style).pack()
    time_entry = tk.Entry(new_window, width=40, **entry_style)
    time_entry.pack(pady=5)

    tk.Button(new_window, text="➕ הוסף משימה", font=("Segoe UI", 12), bg="#198754", fg="white",
              command=lambda: add_task(task_entry, time_entry, listbox)).pack(pady=5)

    tk.Button(new_window, text="✔️ סמן כבוצעה", font=("Segoe UI", 12), bg="#0d6efd", fg="white",
              command=lambda: mark_done(listbox)).pack(pady=5)

    tk.Button(new_window, text="💭 שאלת השראה יומית", font=("Segoe UI", 12), bg="#6f42c1", fg="white",
              command=show_reflection).pack(pady=5)

    tk.Label(new_window, text="📋 רשימת משימות:", **label_style).pack(pady=10)
    listbox = tk.Listbox(new_window, width=50, height=10, font=("Segoe UI", 12))
    listbox.pack(pady=10)

    tk.Button(new_window, text="🚪 יציאה", font=("Segoe UI", 12), bg="#dc3545", fg="white",
              command=new_window.destroy).pack(pady=10)

    update_task_list(listbox)
    check_tasks_for_alerts()


# עיצוב החלון הראשי
def main():
    window.geometry("320x260")
    window.title("ניהול משימות")
    window.config(bg="#0d6d28")

    label_style_main = {"font": ("Segoe UI", 14), "bg": "#0d6d28", "fg": "white"}

    tk.Label(window, text="מה השם שלך?:", **label_style_main).pack(pady=5)
    name_entry = tk.Entry(window, width=30, font=("Segoe UI", 12))
    name_entry.pack()

    tk.Label(window, text="מה הגיל שלך?:", **label_style_main).pack(pady=5)
    age_entry = tk.Entry(window, width=30, font=("Segoe UI", 12))
    age_entry.pack()

    tk.Button(window, text="🚀 התחל", font=("Segoe UI", 13), bg="#198754", fg="white",
              command=open_new_window).pack(pady=15)

    tk.Button(window, text="❌ יציאה", font=("Segoe UI", 13), bg="#dc3545", fg="white",
              command=exit_app).pack()

    # אייקון
    try:
        icon = PhotoImage(file='M.png')
        window.iconphoto(True, icon)
    except:
        pass  # אם אין אייקון

    window.mainloop()

if __name__ == '__main__':
    main()