# Penetration Testing Toolkit
##Overview
A Python-based toolkit that provides essential penetration testing utilities, including a port scanner and a brute-forcer. Designed with a colorful Tkinter GUI for easy use by security professionals and learners.

##Features
-Fast and customizable port scanner

-Simple brute-force attack module

-Colorful and user-friendly Tkinter GUI

-Back buttons for smooth navigation

-Detailed reporting of scan results

## Requirements
Python 3.8+

## Libraries:

tkinter (built-in)

socket

itertools

threading

## Install any missing libraries using:

pip install itertools

## Installation
Clone the repository and run:

python pentest_toolkit.py
## Usage
Launch the toolkit.

Choose the module (Port Scanner or Brute-Forcer).

Enter the required inputs (target host, ports, or credentials list).

View the results and save reports if needed.
## File Structure
penetration-testing-toolkit/
│
├── main.py # Main GUI application
│
├── modules/ # Toolkit modules
│ ├── port_scanner.py # Port scanning module
│ └── brute_forcer.py # Brute-force attack module
│
├── assets/ # Supporting files and resources
│ └── wordlists/ # Contains password wordlists for brute-forcing
