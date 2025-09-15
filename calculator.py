import tkinter as tk
from tkinter import filedialog, messagebox

# ------------------ MAIN WINDOW ------------------
root = tk.Tk()
root.title("✨ GUI Calculator with Notes & History ✨")
root.geometry("900x600")
root.configure(bg="#121212")

# ------------------ HISTORY ------------------
history_list = []

def add_to_history(expression, result):
    history_list.append(f"{expression} = {result}")
    history_box.insert(tk.END, f"{expression} = {result}")
    history_box.yview(tk.END)

def use_history(event):
    selection = history_box.curselection()
    if selection:
        expression = history_list[selection[0]].split("=")[0].strip()
        calc_input.delete(0, tk.END)
        calc_input.insert(tk.END, expression)

# ------------------ CALCULATOR ------------------
def click(btn_text):
    current = calc_input.get()
    calc_input.delete(0, tk.END)
    calc_input.insert(tk.END, current + btn_text)

def clear_calc():
    calc_input.delete(0, tk.END)

def backspace():
    current = calc_input.get()
    calc_input.delete(0, tk.END)
    calc_input.insert(tk.END, current[:-1])   # remove last character

def evaluate():
    try:
        expression = calc_input.get()
        result = str(eval(expression))
        calc_input.delete(0, tk.END)
        calc_input.insert(tk.END, result)
        add_to_history(expression, result)
    except Exception:
        messagebox.showerror("Error", "Invalid Expression")

# ------------------ NOTES ------------------
def save_notes():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(notes_text.get("1.0", tk.END))
        messagebox.showinfo("Saved", "Notes saved successfully!")

def open_notes():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        notes_text.delete("1.0", tk.END)
        notes_text.insert(tk.END, content)

def clear_notes():
    notes_text.delete("1.0", tk.END)

# ------------------ LEFT PANEL: CALCULATOR ------------------
left_frame = tk.Frame(root, bg="#1a1a1a")
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

calc_input = tk.Entry(left_frame, font=("Consolas", 20), borderwidth=5, relief="ridge", justify="right", bg="#222", fg="white")
calc_input.pack(pady=10, padx=10, fill="x")

# Buttons
btns = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
    ("0", ".", "=", "+"),
]

for row_vals in btns:
    row_frame = tk.Frame(left_frame, bg="#1a1a1a")
    row_frame.pack(expand=True, fill="both")
    for val in row_vals:
        if val == "=":
            b = tk.Button(row_frame, text=val, font=("Arial", 16, "bold"),
                          bg="#4CAF50", fg="white", activebackground="#66BB6A",
                          command=evaluate)
        else:
            b = tk.Button(row_frame, text=val, font=("Arial", 16),
                          bg="#333333", fg="white", activebackground="#555555",
                          command=lambda v=val: click(v))
        b.pack(side="left", expand=True, fill="both", padx=2, pady=2)

        # Hover animation
        def on_enter(e, btn=b): btn.config(bg="#555555")
        def on_leave(e, btn=b): 
            if btn["text"] == "=": 
                btn.config(bg="#4CAF50") 
            else: 
                btn.config(bg="#333333")
        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)

# Clear + Backspace row
control_frame = tk.Frame(left_frame, bg="#1a1a1a")
control_frame.pack(fill="x", padx=5, pady=5)

clear_btn = tk.Button(control_frame, text="Clear", font=("Arial", 14, "bold"),
                      bg="#E53935", fg="white", activebackground="#FF5252",
                      command=clear_calc)
clear_btn.pack(side="left", expand=True, fill="x", padx=2)

back_btn = tk.Button(control_frame, text="⌫ Backspace", font=("Arial", 14, "bold"),
                     bg="#FF9800", fg="white", activebackground="#FFB74D",
                     command=backspace)
back_btn.pack(side="left", expand=True, fill="x", padx=2)

# ------------------ RIGHT PANEL: NOTES + HISTORY ------------------
right_frame = tk.Frame(root, bg="#262626")
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Notes
notes_label = tk.Label(right_frame, text="📝 Notes", font=("Arial", 16, "bold"), bg="#262626", fg="white")
notes_label.pack()
notes_text = tk.Text(right_frame, font=("Arial", 14), wrap="word", bg="#111111", fg="white")
notes_text.pack(expand=True, fill="both", padx=10, pady=5)

notes_btn_frame = tk.Frame(right_frame, bg="#262626")
notes_btn_frame.pack()
tk.Button(notes_btn_frame, text="Save", font=("Arial", 12), bg="#4CAF50", fg="white", command=save_notes).pack(side="left", padx=5)
tk.Button(notes_btn_frame, text="Open", font=("Arial", 12), bg="#2196F3", fg="white", command=open_notes).pack(side="left", padx=5)
tk.Button(notes_btn_frame, text="Clear", font=("Arial", 12), bg="#E53935", fg="white", command=clear_notes).pack(side="left", padx=5)

# History
history_label = tk.Label(right_frame, text="📜 History", font=("Arial", 16, "bold"), bg="#262626", fg="white")
history_label.pack(pady=5)
history_box = tk.Listbox(right_frame, font=("Consolas", 12), bg="#111111", fg="lime", height=10)
history_box.pack(fill="both", expand=True, padx=10, pady=5)
history_box.bind("<Double-1>", use_history)

# ------------------ MAINLOOP ------------------
root.mainloop()
