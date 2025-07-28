import tkinter as tk
from tkinter import scrolledtext
import time

def launch(main_root):
    def start_attack():
        output.delete('1.0', tk.END)
        username = user_entry.get().strip()
        target_pass = pass_entry.get().strip()
        found = False

        try:
            with open("assets/wordlist.txt", "r") as f:
                for pwd in f:
                    pwd = pwd.strip()
                    output.insert(tk.END, f"Trying password: {pwd}\n")
                    output.update()
                    time.sleep(0.1)
                    if pwd == target_pass:
                        output.insert(tk.END, f"\n[✔] Password found for {username}: {pwd}\n")
                        found = True
                        break

            if not found:
                output.insert(tk.END, f"\n[✘] Password not found.\n")

        except FileNotFoundError:
            output.insert(tk.END, "[!] Wordlist file not found (assets/wordlist.txt)")

    def go_back():
        win.destroy()
        main_root.deiconify()

    win = tk.Toplevel(main_root)
    win.title("Brute Force Simulator")
    win.geometry("800x550")
    win.configure(bg="#121212")
    main_root.withdraw()

    tk.Label(win, text="Brute Force (SSH Simulator)",
             font=("Segoe UI", 20, "bold"), fg="#00FFEA", bg="#121212").pack(pady=15)

    tk.Label(win, text="Username", font=("Segoe UI", 13),
             fg="#FFFFFF", bg="#121212").pack(pady=5)
    user_entry = tk.Entry(win, width=40, font=("Segoe UI", 13),
                          bg="#1F1F1F", fg="#00FFEA", insertbackground="#00FFEA")
    user_entry.pack(pady=5)

    tk.Label(win, text="Target Password (for testing)", font=("Segoe UI", 13),
             fg="#FFFFFF", bg="#121212").pack(pady=5)
    pass_entry = tk.Entry(win, width=40, show="*", font=("Segoe UI", 13),
                          bg="#1F1F1F", fg="#00FFEA", insertbackground="#00FFEA")
    pass_entry.pack(pady=5)

    tk.Button(win, text="Start Brute Force", command=start_attack,
              bg="#00FFEA", fg="black", font=("Segoe UI", 12, "bold"),
              relief="flat", width=20).pack(pady=15)

    output = scrolledtext.ScrolledText(win, width=85, height=20,
                                       font=("Courier New", 10),
                                       bg="#1F1F1F", fg="#00FFEA")
    output.pack(pady=10)

    tk.Button(win, text="Back", command=go_back,
              bg="#E63946", fg="white", font=("Segoe UI", 12, "bold"),
              relief="flat", width=10).pack(pady=10)
