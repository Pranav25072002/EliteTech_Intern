# Advanced Encryption Tool
## Overview
The Advanced Encryption Tool is a Python-based application that allows users to securely encrypt and decrypt files using the AES-256 encryption algorithm. It features a simple, user-friendly graphical interface built with Tkinter, making file security accessible for all users.

## Features
-AES-256 encryption for strong data security

-Secure file decryption with password protection

-Colorful and intuitive Tkinter-based GUI

-Back buttons for smooth navigation between sections

-Supports multiple file types for encryption and decryption

-Human-friendly design suitable for both beginners and advanced users

## Requirements
Python 3.8 or higher

###Required libraries:

-pycryptodome

-tkinter (usually included with Python)

-os and sys (standard libraries)

### You can install the required library using:

pip install pycryptodome

## Installation
Clone the repository:

git clone https://github.com/yourusername/advanced-encryption-tool.git

cd advanced-encryption-tool

## Run the application:

python advance_encryption_tool.py

## How to Use
Launch the application.

Choose whether to Encrypt or Decrypt a file.

Select the file and enter a secure password.

### For encryption:

The tool will generate an encrypted file in the same directory.

### For decryption:

Enter the correct password to retrieve the original file.

Use the Back button to navigate between the main menu and tool screens.

## Project Structure

advanced-encryption-tool/
│
├── advance_encryption_tool.py  # Main application file
├── README.md                   # Project documentation
└── encrypted_files/            # (Optional) Directory for storing encrypted files

## Future Enhancements
Add drag-and-drop support for easier file selection.

Implement key storage in secure vaults.

Provide multi-file batch encryption and decryption.
