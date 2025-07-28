import tkinter as tk
from modules.port_scanner import launch as launch_port_scanner
from modules.brute_forcer import launch as launch_brute_forcer

class PenTestToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Penetration Testing Toolkit")
        self.root.geometry("1000x600")
        self.root.configure(bg="#121212")

        # Sidebar
        self.sidebar = tk.Frame(root, bg="#1F1F1F", width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.sidebar, text="🛡️ Toolkit", font=("Arial Black", 20),
                 fg="#00FFEA", bg="#1F1F1F").pack(pady=30)

        tk.Button(self.sidebar, text="Home", command=self.show_home,
                  bg="#2D2D2D", fg="#FFFFFF", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)

        tk.Button(self.sidebar, text="Port Scanner", command=self.launch_port_scanner,
                  bg="#2D2D2D", fg="#FFFFFF", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)

        tk.Button(self.sidebar, text="Brute Forcer", command=self.launch_brute_forcer,
                  bg="#2D2D2D", fg="#FFFFFF", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)

        tk.Button(self.sidebar, text="About", command=self.show_about,
                  bg="#2D2D2D", fg="#FFFFFF", font=("Segoe UI", 12, "bold"),
                  relief="flat", width=20).pack(pady=10)

        self.content = tk.Frame(root, bg="#121212")
        self.content.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.show_home()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        tk.Label(self.content, text="Welcome to Penetration Testing Toolkit",
                 font=("Segoe UI", 18, "bold"), fg="#00FFEA", bg="#121212").pack(pady=20)
        tk.Label(self.content, text="Select a tool from the sidebar to get started.",
                 font=("Segoe UI", 14), fg="#FFFFFF", bg="#121212").pack(pady=10)

    def show_about(self):
        self.clear_content()
        tk.Label(self.content, text="About", font=("Segoe UI", 18, "bold"),
                 fg="#00FFEA", bg="#121212").pack(pady=20)
        tk.Label(self.content,
                 text="This toolkit includes:\n• Port Scanner\n• Brute Force (SSH Simulator)\n\n"
                      "Created as part of your cybersecurity learning.",
                 font=("Segoe UI", 13), fg="#FFFFFF", bg="#121212", justify="left").pack(pady=10)

    def launch_port_scanner(self):
        launch_port_scanner(self.root)

    def launch_brute_forcer(self):
        launch_brute_forcer(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = PenTestToolkitApp(root)
    root.mainloop()
