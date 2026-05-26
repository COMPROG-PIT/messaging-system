import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from datetime import datetime

# =========================
# FILE SETUP
# =========================
FILE_NAME = "messages.txt"

if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w").close()

show_state = {"visible": False}

# =========================
# FILE FUNCTIONS
# =========================

def load_messages():
    try:
        messages = []
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "|" in line:
                    parts = line.split("|", 2)
                    if len(parts) == 3:
                        msg_id, msg_time, msg_text = parts
                        messages.append((int(msg_id), msg_time, msg_text))
        return messages

    except Exception as e:
        messagebox.showerror("Error", f"File read error: {e}")
        return []


def save_message(msg):
    try:
        messages = load_messages()

        # safer ID (prevents duplication after delete)
        msg_id = messages[-1][0] + 1 if messages else 1

        # FULL timestamp (date + time)
        time_now = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(f"{msg_id}|{time_now}|{msg}\n")

        return msg_id, time_now

    except Exception as e:
        messagebox.showerror("Error", f"Save error: {e}")


def rewrite_file(messages):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            for i, (_, t, msg) in enumerate(messages, start=1):
                f.write(f"{i}|{t}|{msg}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Rewrite error: {e}")


# =========================
# FEATURES
# =========================

def send_message():
    msg = entry.get().strip()

    if not msg:
        messagebox.showwarning("Warning 💔", "Message cannot be empty!")
        return

    msg_id, time_now = save_message(msg)
    entry.delete(0, tk.END)

    messagebox.showinfo("Saved 💌", f"Message saved #{msg_id} at {time_now}")
    show_messages()


def show_messages():
    listbox.delete(0, tk.END)
    messages = load_messages()

    if not messages:
        listbox.insert(tk.END, "💔 No messages yet...")
        return

    for msg_id, time, msg in messages:
        if show_state["visible"]:
            listbox.insert(tk.END, f"💌 Message {msg_id}: {msg} ({time})")
        else:
            listbox.insert(tk.END, f"📜 Message {msg_id} (hidden)")


def toggle_show():
    show_state["visible"] = not show_state["visible"]
    show_messages()


def delete_message():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning 🗑️", "Select a message first!")
        return

    index = selected[0]
    messages = load_messages()

    if index < len(messages):
        messages.pop(index)
        rewrite_file(messages)

    show_messages()


def search_message():
    keyword = simpledialog.askstring("Search 🔍", "Enter keyword:")

    if not keyword:
        return

    keyword = keyword.lower()
    listbox.delete(tk.END)

    messages = load_messages()
    found = False

    for msg_id, time, msg in messages:
        if keyword in msg.lower():
            listbox.insert(tk.END, f"💖 {msg} ({time})")
            found = True

    if not found:
        listbox.insert(tk.END, "😢 No match found")


# =========================
# UI DESIGN
# =========================

root = tk.Tk()
root.title("💬 Pink Messenger")
root.geometry("520x650")
root.configure(bg="#ffd6e8")

# HEADER
header = tk.Frame(root, bg="#ff4da6", height=100)
header.pack(fill="x")

tk.Label(
    header,
    text="💬 Pink Messenger",
    font=("Helvetica", 20, "bold"),
    bg="#ff4da6",
    fg="white"
).pack(pady=5)

tk.Label(
    header,
    text="Send, store, and manage messages 💌",
    bg="#ff4da6",
    fg="white"
).pack()

# INPUT
input_card = tk.Frame(root, bg="white")
input_card.pack(pady=15, padx=15, fill="x")

entry = tk.Entry(input_card, font=("Arial", 13), bd=0)
entry.pack(padx=12, pady=12, fill="x")

tk.Button(
    input_card,
    text="💌 Send Message",
    bg="#ff4da6",
    fg="white",
    font=("Arial", 11, "bold"),
    bd=0,
    command=send_message
).pack(pady=5)

# BUTTONS
btn_frame = tk.Frame(root, bg="#ffd6e8")
btn_frame.pack(pady=10)

btn_style = {
    "font": ("Arial", 10, "bold"),
    "fg": "white",
    "bd": 0,
    "width": 16
}

tk.Button(btn_frame, text="📜 Show Messages",
          bg="#ff66b2", command=toggle_show, **btn_style).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="🔍 Search",
          bg="#ff99cc", command=search_message, **btn_style).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="🗑️ Delete",
          bg="#ff3385", command=delete_message, **btn_style).grid(row=0, column=2, padx=5)

# CHAT AREA
chat_frame = tk.Frame(root, bg="white")
chat_frame.pack(padx=15, pady=15, fill="both", expand=True)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(
    chat_frame,
    font=("Arial", 11),
    bg="white",
    fg="#333",
    selectbackground="#ffb6d9",
    bd=0,
    yscrollcommand=scrollbar.set
)

listbox.pack(fill="both", expand=True, padx=10, pady=10)
scrollbar.config(command=listbox.yview)

# INIT
show_messages()
root.mainloop()