#!/usr/bin/env python3
"""
CCLI - Custom Command Line Interface
Main entry point for the application
"""

import tkinter as tk
from gui import CCLIGUI

def main():
    """Initialize and run the CCLI application"""
    root = tk.Tk()
    app = CCLIGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()