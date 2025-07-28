import socket
import tkinter as tk
from tkinter import scrolledtext
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

def launch(main_root):
    def start_scan():
        output.delete('1.0', tk.END)
        target = target_entry.get().strip()

        try:
            ip = socket.gethostbyname(target)
            output.insert(tk.END, f"[*] Scanning {ip}...\n")

            threading.Thread(target=scan_ports, args=(ip,), daemon=True).start()
            win.after(100, update_output_box)
        except socket.gaierror:
            output.insert(tk.END, "[!] Invalid hostname or IP address\n")
        except Exception as e:
            output.insert(tk.END, f"[!] Error: {e}\n")

    def scan_ports(ip):
        with ThreadPoolExecutor(max_workers=100) as executor:
            for port in range(1, 1025):
                executor.submit(scan_port, ip, port)

    def scan_port(ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            result = sock.connect_ex((ip, port))
            if result == 0:
                result_queue.put(f"[+] Port {port} is OPEN")
            sock.close()
        except Exception as e:
            result_queue.put(f"[!] Error scanning port {port}: {e}")

    def update_output_box():
        try:
            while True:
                line = result_queue.get_nowait()
                output.insert(tk.END, line + "\n")
                output.see(tk.END)
        except queue.Empty:
            pass
        win.after(100, update_output_box)

    def go_back():
        win.destroy()
        main_root.deiconify()

    win = tk.Toplevel(main_root)
    win.title("Port Scanner")
    win.geometry("800x550")
    win.configure(bg="#121212")
    main_root.withdraw()

    tk.Label(win, text="Port Scanner", font=("Segoe UI", 20, "bold"),
             fg="#00FFEA", bg="#121212").pack(pady=15)

    tk.Label(win, text="Target Host/IP:", font=("Segoe UI", 13),
             fg="#FFFFFF", bg="#121212").pack(pady=5)
    target_entry = tk.Entry(win, width=40, font=("Segoe UI", 13),
                            bg="#1F1F1F", fg="#00FFEA", insertbackground="#00FFEA")
    target_entry.pack(pady=5)

    tk.Button(win, text="Start Scan", command=start_scan,
              bg="#00FFEA", fg="black", font=("Segoe UI", 12, "bold"),
              relief="flat", width=15).pack(pady=15)

    output = scrolledtext.ScrolledText(win, width=85, height=20,
                                       font=("Courier New", 10),
                                       bg="#1F1F1F", fg="#00FFEA")
    output.pack(pady=10)

    tk.Button(win, text="Back", command=go_back,
              bg="#E63946", fg="white", font=("Segoe UI", 12, "bold"),
              relief="flat", width=10).pack(pady=10)

    result_queue = queue.Queue()
