# Overview
A lightweight Python tool that monitors files for unauthorized changes by calculating and comparing cryptographic hash values (SHA-256). Designed to help users detect tampering or accidental modifications.

## Features
-Tracks changes in files using SHA-256 hashes

-Simple and clean Tkinter-based GUI

-Monitors multiple files or directories

-Easy-to-use and lightweight

## Requirements

Python 3.8+

## Libraries:

tkinter (built-in)

hashlib and os (built-in)

## Installation
Clone the repository and run:

python file_integrity_checker.py

## How It Works

Select files or directories to monitor.

The tool stores baseline hash values.

On re-check, it compares current hashes with the stored ones.

Any change triggers an alert.
