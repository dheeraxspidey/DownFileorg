#!/usr/bin/env python3
"""
Minimal GUI Test - Just to verify organize button appears
"""

import tkinter as tk
from pathlib import Path

def test_organize():
    print("Organize button clicked!")

# Create test GUI
root = tk.Tk()
root.title("🗂️ Test File Organizer")
root.geometry("500x450")
root.configure(bg='#f0f0f0')

# Title
title_frame = tk.Frame(root, bg='#2c3e50', height=60)
title_frame.pack(fill='x')
title_frame.pack_propagate(False)

title_label = tk.Label(title_frame, text="🗂️ File Organizer TEST", font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
title_label.pack(expand=True)

# Main frame
main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(fill='both', expand=True, padx=15, pady=10)

# Instruction
instruction = tk.Label(main_frame, text="Test GUI - The organize button should be visible below", font=('Arial', 11), fg='#2c3e50', bg='#f0f0f0')
instruction.pack(pady=(0, 15))

# Folder frame
folder_frame = tk.LabelFrame(main_frame, text="📁 Folder", font=('Arial', 11, 'bold'), padx=10, pady=10, bg='#ecf0f1')
folder_frame.pack(fill='x', pady=(0, 15))

downloads_path = str(Path.home() / "Downloads")
path_var = tk.StringVar(value=downloads_path)
path_entry = tk.Entry(folder_frame, textvariable=path_var, font=('Arial', 10), state='readonly', bg='white')
path_entry.pack(fill='x')

# Progress bar placeholder
progress_label = tk.Label(main_frame, text="Progress bar would be here", font=('Arial', 10), fg='#7f8c8d', bg='#f0f0f0')
progress_label.pack(pady=(0, 15))

# THE ORGANIZE BUTTON - This is what should be visible
organize_btn = tk.Button(
    main_frame,
    text="🚀 ORGANIZE FILES - CLICK ME!",
    command=test_organize,
    bg='#27ae60',
    fg='white',
    font=('Arial', 14, 'bold'),
    pady=12,
    relief='flat',
    cursor='hand2'
)
organize_btn.pack(fill='x', pady=(10, 10))

# Stats
stats_label = tk.Label(main_frame, text="📊 Files in Downloads: 0", font=('Arial', 10), fg='#7f8c8d', bg='#f0f0f0')
stats_label.pack()

print("✅ Test GUI created - Organize button should be visible!")
print(f"Window size: {root.geometry()}")
print(f"Organize button text: {organize_btn['text']}")

# Center window
root.update_idletasks()
x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
root.geometry(f"+{x}+{y}")

root.mainloop()
