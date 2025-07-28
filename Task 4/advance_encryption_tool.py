import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

# ======= AES Utility Functions =======
def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=32, count=1000000)

def encrypt_file(filepath, password):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        salt = get_random_bytes(16)
        key = derive_key(password.encode(), salt)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        encrypted_data = salt + iv + ciphertext
        encrypted_filepath = filepath + '.enc'
        with open(encrypted_filepath, 'wb') as f:
            f.write(encrypted_data)
        return encrypted_filepath
    except Exception as e:
        return str(e)

def decrypt_file(filepath, password):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        salt, iv, ciphertext = content[:16], content[16:32], content[32:]
        key = derive_key(password.encode(), salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        decrypted_filepath = filepath.replace('.enc', '')
        with open(decrypted_filepath, 'wb') as f:
            f.write(decrypted_data)
        return decrypted_filepath
    except Exception as e:
        return str(e)

# ======= Main Dashboard App =======
class AdvancedEncryptionDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced AES-256 Encryption Tool")
        self.root.geometry("1000x600")
        self.root.configure(bg="#121212")
        self.file_path = None

        # Sidebar
        self.sidebar = tk.Frame(root, bg="#1F1F1F", width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self.sidebar, text="🔐 Encryptor", font=("Arial Black", 20),
                 fg="#00FFEA", bg="#1F1F1F").pack(pady=30)
        tk.Button(self.sidebar, text="Home", command=self.show_home,
                  bg="#2D2D2D", fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)
        tk.Button(self.sidebar, text="Encrypt File", command=self.show_encrypt_page,
                  bg="#2D2D2D", fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)
        tk.Button(self.sidebar, text="Decrypt File", command=self.show_decrypt_page,
                  bg="#2D2D2D", fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)
        tk.Button(self.sidebar, text="About", command=self.show_about,
                  bg="#2D2D2D", fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)

        # Main content area
        self.content = tk.Frame(root, bg="#121212")
        self.content.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.show_home()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        tk.Label(self.content, text="Welcome to AES-256 Encryption Tool",
                 font=("Segoe UI", 18, "bold"), fg="#00FFEA", bg="#121212").pack(pady=20)
        tk.Label(self.content, text="Use the sidebar to encrypt or decrypt your files securely.",
                 font=("Segoe UI", 14), fg="white", bg="#121212").pack(pady=10)

    def show_encrypt_page(self):
        self.clear_content()
        tk.Label(self.content, text="Encrypt a File", font=("Segoe UI", 18, "bold"),
                 fg="#00FFEA", bg="#121212").pack(pady=20)

        file_entry = tk.Entry(self.content, width=50, font=("Segoe UI", 12),
                              bg="#1F1F1F", fg="#00FFEA", insertbackground="#00FFEA")
        file_entry.pack(pady=5)

        def browse_file():
            self.file_path = filedialog.askopenfilename()
            file_entry.delete(0, tk.END)
            file_entry.insert(0, self.file_path)

        tk.Button(self.content, text="Browse File 📁", command=browse_file,
                  bg="#00FFEA", fg="black", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=5)

        password_entry = tk.Entry(self.content, show="*", width=35, font=("Segoe UI", 12),
                                  bg="#1F1F1F", fg="#00FFEA", insertbackground="#00FFEA")
        password_entry.pack(pady=10)
        tk.Label(self.content, text="Enter Password", font=("Segoe UI", 11),
                 fg="white", bg="#121212").pack(pady=5)

        status_label = tk.Label(self.content, text="", fg="#06D6A0", bg="#121212",
                                font=("Segoe UI", 10, "italic"))
        status_label.pack(pady=10)

        def encrypt_action():
            if not self.file_path or not password_entry.get():
                messagebox.showwarning("Missing Info", "Please select a file and enter a password.")
                return
            result = encrypt_file(self.file_path, password_entry.get())
            if os.path.exists(result):
                status_label.config(text=f"File encrypted successfully:\n{result}", fg="#06D6A0")
            else:
                status_label.config(text=f"Error: {result}", fg="#E63946")

        tk.Button(self.content, text="Encrypt 🔐", command=encrypt_action,
                  bg="#4CD137", fg="black", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)

        tk.Button(self.content, text="Back", command=self.show_home,
                  bg="#E63946", fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=15).pack(pady=20)

    def show_decrypt_page(self):
        self.clear_content()
        tk.Label(self.content, text="Decrypt a File", font=("Segoe UI", 18, "bold"),
                 fg="#00FFEA", bg="#121212").pack(pady=20)

        file_entry = tk.Entry(self.content, width=50, font=("Segoe UI", 12),
                              bg="#1F1F1F", fg="#00FFEA", insertbackground="#00FFEA")
        file_entry.pack(pady=5)

        def browse_file():
            self.file_path = filedialog.askopenfilename()
            file_entry.delete(0, tk.END)
            file_entry.insert(0, self.file_path)

        tk.Button(self.content, text="Browse File 📁", command=browse_file,
                  bg="#00FFEA", fg="black", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=5)

        password_entry = tk.Entry(self.content, show="*", width=35, font=("Segoe UI", 12),
                                  bg="#1F1F1F", fg="#00FFEA", insertbackground="#00FFEA")
        password_entry.pack(pady=10)
        tk.Label(self.content, text="Enter Password", font=("Segoe UI", 11),
                 fg="white", bg="#121212").pack(pady=5)

        status_label = tk.Label(self.content, text="", fg="#06D6A0", bg="#121212",
                                font=("Segoe UI", 10, "italic"))
        status_label.pack(pady=10)

        def decrypt_action():
            if not self.file_path or not password_entry.get():
                messagebox.showwarning("Missing Info", "Please select a file and enter a password.")
                return
            result = decrypt_file(self.file_path, password_entry.get())
            if os.path.exists(result):
                status_label.config(text=f"File decrypted successfully:\n{result}", fg="#06D6A0")
            else:
                status_label.config(text=f"Error: {result}", fg="#E63946")

        tk.Button(self.content, text="Decrypt 🔓", command=decrypt_action,
                  bg="#4CD137", fg="black", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)

        tk.Button(self.content, text="Back", command=self.show_home,
                  bg="#E63946", fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=15).pack(pady=20)

    def show_about(self):
        self.clear_content()
        tk.Label(self.content, text="About", font=("Segoe UI", 18, "bold"),
                 fg="#00FFEA", bg="#121212").pack(pady=20)
        tk.Label(self.content,
                 text="Advanced AES-256 Encryption Tool\n\nEncrypt and decrypt files with military-grade security.\n"
                      "Cybersecurity Dashboard Edition.",
                 font=("Segoe UI", 13), fg="white", bg="#121212", justify="left").pack(pady=10)
        tk.Button(self.content, text="Back", command=self.show_home,
                  bg="#E63946", fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=15).pack(pady=20)

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedEncryptionDashboard(root)
    root.mainloop()
