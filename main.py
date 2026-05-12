from tkinter import *
from tkinter import messagebox

FILE_NAME = "messages.txt"

# ---------------- FUNCTIONS ---------------- #

def send_message():
    message = entry.get()

    if message.strip() == "":
        messagebox.showerror("Error", "Message cannot be empty!")
        return

    try:
        with open(FILE_NAME, "a") as file:
            file.write(message + "\n")

        entry.delete(0, END)
        display_messages()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def display_messages():
    listbox.delete(0, END)

    try:
        with open(FILE_NAME, "r") as file:
            messages = file.readlines()

            for msg in messages:
                listbox.insert(END, msg.strip())

    except FileNotFoundError:
        open(FILE_NAME, "w").close()


def delete_message():
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a message first!")
        return

    try:
        with open(FILE_NAME, "r") as file:
            messages = file.readlines()

        del messages[selected[0]]

        with open(FILE_NAME, "w") as file:
            file.writelines(messages)

        display_messages()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def search_message():
    keyword = entry.get().lower()

    listbox.delete(0, END)

    try:
        with open(FILE_NAME, "r") as file:
            messages = file.readlines()

            for msg in messages:
                if keyword in msg.lower():
                    listbox.insert(END, msg.strip())

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- GUI ---------------- #

root = Tk()
root.title("Messaging System")
root.geometry("500x400")

Label(root, text="Enter Message:", font=("Arial", 12)).pack(pady=5)

entry = Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5)

Button(root, text="Send Message", command=send_message).pack(pady=5)
Button(root, text="Display Messages", command=display_messages).pack(pady=5)
Button(root, text="Delete Message", command=delete_message).pack(pady=5)
Button(root, text="Search Message", command=search_message).pack(pady=5)

listbox = Listbox(root, width=60, height=12)
listbox.pack(pady=10)

display_messages()

root.mainloop()