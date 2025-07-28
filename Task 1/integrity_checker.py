import hashlib
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

HASH_DB_FILE = 'hash_database.json'

# ========== HASH CALCULATION ==========
def calculate_hash(filepath, algorithm='sha256'):
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

# ========== DATABASE HANDLING ==========
def load_hash_database():
    if os.path.exists(HASH_DB_FILE):
        with open(HASH_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hash_database(db):
    with open(HASH_DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

# ========== DIRECTORY MONITORING ==========
def monitor_directory(directory, output_box, progress_bar, status_labels):
    hash_db = load_hash_database()
    updated_db = {}
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    scanned_files = 0
    new_count = mod_count = unchanged_count = removed_count = 0

    output_box.insert(tk.END, f"\n[INFO] Scanning directory: {directory}\n")
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)
            updated_db[filepath] = file_hash

            if filepath not in hash_db:
                output_box.insert(tk.END, f"[NEW FILE] {filepath}\n")
                new_count += 1
            elif hash_db[filepath] != file_hash:
                output_box.insert(tk.END, f"[MODIFIED] {filepath}\n")
                mod_count += 1
            else:
                unchanged_count += 1
            scanned_files += 1

            progress_bar['value'] = (scanned_files / total_files) * 100
            progress_bar.update()
            output_box.update()

    removed_files = set(hash_db.keys()) - set(updated_db.keys())
    for filepath in removed_files:
        output_box.insert(tk.END, f"[REMOVED] {filepath}\n")
        removed_count += 1

    save_hash_database(updated_db)
    output_box.insert(tk.END, "\n[INFO] Scan complete.\n")

    # Update status panel
    status_labels['scanned'].config(text=f"Scanned: {scanned_files}")
    status_labels['new'].config(text=f"New: {new_count}")
    status_labels['modified'].config(text=f"Modified: {mod_count}")
    status_labels['removed'].config(text=f"Removed: {removed_count}")

# ========== GUI ==========
def start_gui():
    def select_directory():
        directory = filedialog.askdirectory()
        if directory:
            dir_entry.delete(0, tk.END)
            dir_entry.insert(0, directory)

    def start_scan():
        directory = dir_entry.get().strip()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory path!")
            return
        output_box.delete('1.0', tk.END)
        progress_bar['value'] = 0
        monitor_directory(directory, output_box, progress_bar, status_labels)

    root = tk.Tk()
    root.title("File Integrity Checker")
    root.geometry("1000x600")
    root.configure(bg="#f3f3f3")

    # Left Panel (controls)
    left_panel = tk.Frame(root, bg="#2b2d42", width=250, height=600)
    left_panel.pack(side=tk.LEFT, fill=tk.Y)

    tk.Label(left_panel, text="Integrity Checker", font=("Arial Black", 16),
             fg="#f3f3f3", bg="#2b2d42").pack(pady=20)

    dir_entry = tk.Entry(left_panel, width=25, font=("Segoe UI", 11))
    dir_entry.pack(pady=10, padx=20)

    browse_btn = tk.Button(left_panel, text="Browse", command=select_directory,
                           bg="#8d99ae", fg="white", font=("Segoe UI", 10, "bold"),
                           relief="flat", width=15)
    browse_btn.pack(pady=5)

    scan_btn = tk.Button(left_panel, text="Start Scan", command=start_scan,
                         bg="#ef233c", fg="white", font=("Segoe UI", 11, "bold"),
                         relief="flat", width=15)
    scan_btn.pack(pady=10)

    # Stats panel
    status_labels = {
        'scanned': tk.Label(left_panel, text="Scanned: 0", fg="white", bg="#2b2d42", font=("Segoe UI", 10)),
        'new': tk.Label(left_panel, text="New: 0", fg="#06d6a0", bg="#2b2d42", font=("Segoe UI", 10)),
        'modified': tk.Label(left_panel, text="Modified: 0", fg="#ffd166", bg="#2b2d42", font=("Segoe UI", 10)),
        'removed': tk.Label(left_panel, text="Removed: 0", fg="#ef476f", bg="#2b2d42", font=("Segoe UI", 10)),
    }
    for lbl in status_labels.values():
        lbl.pack(pady=5)

    # Right Panel (output and progress)
    right_panel = tk.Frame(root, bg="#f3f3f3")
    right_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    progress_bar = ttk.Progressbar(right_panel, orient="horizontal", length=600, mode="determinate")
    progress_bar.pack(pady=15)

    output_box = scrolledtext.ScrolledText(right_panel, width=90, height=25,
                                           font=("Courier New", 10), bg="#edf2f4", fg="#2b2d42")
    output_box.pack(pady=10, padx=20, expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
