#!/usr/bin/env python3
"""
Simple File Organizer GUI
Organizes files in Downloads folder automatically using AI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
import shutil
from pathlib import Path
from random_forest_classifier import RandomForestFileClassifier

class SimpleFileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI File Organizer Pro")
        self.root.geometry("600x550")
        self.root.configure(bg='#0a0e27')  # Dark blue background
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.colors = {
            'primary': '#6C5CE7',      # Purple
            'secondary': '#74B9FF',    # Light blue
            'accent': '#00CEC9',       # Teal
            'success': '#00B894',      # Green
            'warning': '#FDCB6E',      # Yellow
            'danger': '#E17055',       # Red
            'dark': '#0a0e27',         # Dark blue
            'light': '#FFFFFF',        # White
            'grey': '#636E72',         # Grey
            'card': '#1e2139',         # Dark card
            'text': '#DDD6FE'          # Light text
        }
        
        # Initialize classifier
        self.classifier = None
        self.load_classifier()
        
        # Default to Downloads folder
        self.downloads_path = str(Path.home() / "Downloads")
        
        # Create modern GUI
        self.create_modern_widgets()
        
    def load_classifier(self):
        """Load the trained Random Forest classifier."""
        try:
            self.classifier = RandomForestFileClassifier()
            
            # Get the correct path for the model file
            if getattr(sys, 'frozen', False):
                # Running as executable
                bundle_dir = sys._MEIPASS
                model_path = os.path.join(bundle_dir, 'rf_file_classifier.joblib')
            else:
                # Running as script
                model_path = 'rf_file_classifier.joblib'
            
            if os.path.exists(model_path):
                self.classifier.load_model(model_path)
                print("✅ Classifier loaded successfully")
            else:
                messagebox.showerror("Error", f"Model file not found at: {model_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classifier: {e}")
    
    def create_modern_widgets(self):
        """Create modern, sleek GUI widgets."""
        
        # Top header with gradient effect
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['dark'])
        header_content.pack(expand=True, fill='both', padx=30, pady=15)
        
        # App icon and title
        title_frame = tk.Frame(header_content, bg=self.colors['dark'])
        title_frame.pack(side='left', fill='y')
        
        app_icon = tk.Label(
            title_frame,
            text="🤖",
            font=('Segoe UI', 24),
            bg=self.colors['dark'],
            fg=self.colors['accent']
        )
        app_icon.pack(side='left', padx=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="AI File Organizer Pro",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['dark'],
            fg=self.colors['light']
        )
        title_label.pack(side='left', anchor='w')
        
        # Status indicator
        self.status_indicator = tk.Label(
            header_content,
            text="🟢 Ready",
            font=('Segoe UI', 10),
            bg=self.colors['dark'],
            fg=self.colors['success']
        )
        self.status_indicator.pack(side='right', anchor='e')
        
        # Main container with cards
        main_container = tk.Frame(self.root, bg=self.colors['dark'])
        main_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Welcome card
        welcome_card = self.create_card(main_container)
        welcome_card.pack(fill='x', pady=(0, 20))
        
        welcome_icon = tk.Label(
            welcome_card,
            text="✨",
            font=('Segoe UI', 20),
            bg=self.colors['card'],
            fg=self.colors['warning']
        )
        welcome_icon.pack(pady=(10, 5))
        
        welcome_text = tk.Label(
            welcome_card,
            text="Intelligent file organization powered by AI",
            font=('Segoe UI', 12),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        welcome_text.pack(pady=(0, 15))
        
        # Folder selection card
        folder_card = self.create_card(main_container)
        folder_card.pack(fill='x', pady=(0, 20))
        
        folder_title = tk.Label(
            folder_card,
            text="📁 Select Target Directory",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['light']
        )
        folder_title.pack(pady=(15, 10), anchor='w', padx=20)
        
        # Path frame
        path_frame = tk.Frame(folder_card, bg=self.colors['card'])
        path_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        self.folder_var = tk.StringVar(value=self.downloads_path)
        path_entry = tk.Entry(
            path_frame,
            textvariable=self.folder_var,
            font=('Segoe UI', 10),
            bg='#2d3748',
            fg=self.colors['text'],
            border=0,
            relief='flat',
            insertbackground=self.colors['text']
        )
        path_entry.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))
        
        browse_btn = self.create_modern_button(
            path_frame,
            "Browse",
            self.colors['secondary'],
            self.browse_folder,
            width=80
        )
        browse_btn.pack(side='right')
        
        # Stats card
        stats_card = self.create_card(main_container)
        stats_card.pack(fill='x', pady=(0, 20))
        
        stats_frame = tk.Frame(stats_card, bg=self.colors['card'])
        stats_frame.pack(fill='x', padx=20, pady=15)
        
        # File count
        file_icon = tk.Label(
            stats_frame,
            text="📊",
            font=('Segoe UI', 16),
            bg=self.colors['card'],
            fg=self.colors['accent']
        )
        file_icon.pack(side='left', padx=(0, 10))
        
        self.stats_label = tk.Label(
            stats_frame,
            text=f"Files detected: {self.count_files()}",
            font=('Segoe UI', 12),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        self.stats_label.pack(side='left')
        
        # Progress card
        progress_card = self.create_card(main_container)
        progress_card.pack(fill='x', pady=(0, 20))
        
        # Progress bar with custom styling
        progress_label = tk.Label(
            progress_card,
            text="🔄 Organization Progress",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['light']
        )
        progress_label.pack(pady=(15, 10), padx=20, anchor='w')
        
        progress_container = tk.Frame(progress_card, bg=self.colors['card'])
        progress_container.pack(fill='x', padx=20, pady=(0, 15))
        
        # Custom progress bar
        self.progress_bg = tk.Frame(
            progress_container,
            bg='#2d3748',
            height=8
        )
        self.progress_bg.pack(fill='x')
        
        self.progress_bar = tk.Frame(
            self.progress_bg,
            bg=self.colors['accent'],
            height=8
        )
        
        self.status_text = tk.Label(
            progress_container,
            text="Ready to organize files",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['grey']
        )
        self.status_text.pack(pady=(8, 0), anchor='w')
        
        # Action buttons
        button_frame = tk.Frame(main_container, bg=self.colors['dark'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Main organize button
        self.organize_btn = self.create_gradient_button(
            button_frame,
            "🚀 Organize Files",
            self.colors['primary'],
            self.colors['secondary'],
            self.organize_files
        )
        self.organize_btn.pack(fill='x')
        
    def create_card(self, parent):
        """Create a modern card-like frame."""
        card = tk.Frame(
            parent,
            bg=self.colors['card'],
            relief='flat',
            bd=0
        )
        # Add shadow effect by creating a slightly larger dark frame
        shadow = tk.Frame(
            parent,
            bg='#0d1117',
            height=2
        )
        return card
    
    def create_modern_button(self, parent, text, color, command, width=None):
        """Create a modern styled button."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            border=0,
            relief='flat',
            cursor='hand2',
            activebackground=self.darken_color(color),
            activeforeground='white'
        )
        if width:
            btn.config(width=width//8)  # Approximate width conversion
        return btn
    
    def create_gradient_button(self, parent, text, color1, color2, command):
        """Create a gradient-style button."""
        btn_frame = tk.Frame(parent, bg=color1, relief='flat', bd=0)
        
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            bg=color1,
            fg='white',
            font=('Segoe UI', 14, 'bold'),
            border=0,
            relief='flat',
            cursor='hand2',
            activebackground=color2,
            activeforeground='white',
            pady=12
        )
        btn.pack(fill='both', expand=True)
        
        return btn_frame
    
    def darken_color(self, color):
        """Darken a hex color for hover effects."""
        # Simple color darkening
        color_map = {
            self.colors['primary']: '#5A52D5',
            self.colors['secondary']: '#5A9FE7',
            self.colors['accent']: '#00A59B',
            self.colors['success']: '#009B7D'
        }
        return color_map.get(color, color)
    
    def update_progress(self, percentage):
        """Update the custom progress bar."""
        if hasattr(self, 'progress_bar'):
            self.progress_bar.place(relwidth=percentage/100, relheight=1)
        folder_entry = tk.Entry(
            folder_frame,
            textvariable=self.folder_var,
            font=('Arial', 10),
            width=50,
            state='readonly',
            bg='white'
        )
        folder_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Browse button
        browse_btn = tk.Button(
            folder_frame,
            text="Browse",
            command=self.browse_folder,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            relief='flat'
        )
        browse_btn.pack(side='right')
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg='#f0f0f0')
        progress_frame.pack(fill='x', pady=(0, 15))
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            style='TProgressbar'
        )
        self.progress.pack(fill='x')
        
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to organize files",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='#f0f0f0'
        )
        self.status_label.pack(pady=(10, 0))
        
        # Organize button
        self.organize_btn = tk.Button(
            main_frame,
            text="🚀 Organize Files",
            command=self.organize_files,
            bg='#27ae60',
            fg='white',
            font=('Arial', 14, 'bold'),
            pady=12,
            relief='flat',
            cursor='hand2'
        )
        self.organize_btn.pack(fill='x', pady=(0, 10))
        print("✅ Organize button created and packed")  # Debug output
        
        # Quick stats
        stats_frame = tk.Frame(main_frame, bg='#f0f0f0')
        stats_frame.pack(fill='x')
        
        self.stats_label = tk.Label(
            stats_frame,
            text=f"📊 Files in folder: {self.count_files()}",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='#f0f0f0'
        )
        self.stats_label.pack()
    
    def browse_folder(self):
        """Browse for a folder to organize."""
        folder = filedialog.askdirectory(
            title="Select folder to organize",
            initialdir=self.downloads_path
        )
        if folder:
            self.folder_var.set(folder)
            self.downloads_path = folder
            self.stats_label.config(text=f"📊 Files in folder: {self.count_files()}")
    
    def count_files(self):
        """Count files in the selected folder."""
        try:
            if os.path.exists(self.downloads_path):
                files = [f for f in os.listdir(self.downloads_path) 
                        if os.path.isfile(os.path.join(self.downloads_path, f))]
                return len(files)
        except:
            pass
        return 0
    
    def organize_files(self):
        """Organize files in the selected folder."""
        if not self.classifier:
            messagebox.showerror("Error", "Classifier not loaded!")
            return
        
        if not os.path.exists(self.downloads_path):
            messagebox.showerror("Error", "Selected folder does not exist!")
            return
        
        # Disable button and start progress
        self.organize_btn.config(state='disabled', text="Organizing...", bg='#95a5a6')
        self.progress.start(10)
        self.status_label.config(text="Scanning files...", fg='#3498db')
        
        # Run organization in separate thread
        thread = threading.Thread(target=self._organize_worker)
        thread.daemon = True
        thread.start()
    
    def _organize_worker(self):
        """Worker thread for file organization."""
        try:
            # Get all files in the folder
            files = []
            for item in os.listdir(self.downloads_path):
                item_path = os.path.join(self.downloads_path, item)
                if os.path.isfile(item_path):
                    files.append(item_path)
            
            if not files:
                self.root.after(0, lambda: self._show_completion("No files to organize!"))
                return
            
            # Create organized folders
            organized_count = 0
            categories = set()
            
            for i, file_path in enumerate(files):
                try:
                    # Update status
                    self.root.after(0, lambda f=os.path.basename(file_path): 
                                   self.status_label.config(text=f"Processing: {f[:30]}..."))
                    
                    # Classify file
                    result = self.classifier.predict(file_path)
                    category = result['predicted_category']
                    folder_name = result.get('folder_name', category)
                    categories.add(folder_name)
                    
                    # Smart folder management - check for existing similar folders
                    category_folder = self._get_or_create_folder(folder_name)
                    
                    # Move file to category folder
                    destination = os.path.join(category_folder, os.path.basename(file_path))
                    
                    # Handle name conflicts
                    counter = 1
                    base_name, ext = os.path.splitext(os.path.basename(file_path))
                    while os.path.exists(destination):
                        new_name = f"{base_name}_{counter}{ext}"
                        destination = os.path.join(category_folder, new_name)
                        counter += 1
                    
                    shutil.move(file_path, destination)
                    organized_count += 1
                    
                except Exception as e:
                    print(f"Error organizing {file_path}: {e}")
                    continue
            
            # Show completion message
            message = f"✅ Successfully organized {organized_count} files into {len(categories)} categories:\n"
            message += ", ".join(sorted(categories))
            
            self.root.after(0, lambda: self._show_completion(message))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_completion(f"❌ Error: {e}"))
    
    def _show_completion(self, message):
        """Show completion message and reset UI."""
        self.progress.stop()
        self.organize_btn.config(state='normal', text="🚀 Organize Files", bg='#27ae60')
        self.status_label.config(text="Ready to organize files", fg='#7f8c8d')
        self.stats_label.config(text=f"📊 Files in folder: {self.count_files()}")
        
        messagebox.showinfo("Organization Complete", message)
    
    def _get_or_create_folder(self, folder_name: str) -> str:
        """Get existing folder or create new one if needed."""
        folder_path = os.path.join(self.downloads_path, folder_name)
        
        # Check if exact folder exists
        if os.path.exists(folder_path):
            return folder_path
        
        # Check for similar existing folders (case-insensitive)
        existing_folders = [item for item in os.listdir(self.downloads_path) 
                           if os.path.isdir(os.path.join(self.downloads_path, item)) 
                           and not item.startswith('.')]
        
        for existing_folder in existing_folders:
            if existing_folder.lower() == folder_name.lower():
                existing_path = os.path.join(self.downloads_path, existing_folder)
                print(f"📁 Using existing folder: {existing_folder}")
                return existing_path
        
        # Check for partial matches (e.g., "Education" vs "Education and Finance")
        folder_name_lower = folder_name.lower()
        for existing_folder in existing_folders:
            existing_lower = existing_folder.lower()
            
            # If new folder name contains existing folder name or vice versa
            if (folder_name_lower in existing_lower or existing_lower in folder_name_lower):
                existing_path = os.path.join(self.downloads_path, existing_folder)
                print(f"📁 Using similar existing folder: {existing_folder} (for {folder_name})")
                return existing_path
        
        # Create new folder
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"📁 Created new folder: {folder_name}")
            return folder_path
        except Exception as e:
            print(f"❌ Failed to create folder {folder_name}: {e}")
            # Fallback to Downloads root
            return self.downloads_path

def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    
    # Configure ttk style for better looking progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TProgressbar', background='#3498db', troughcolor='#ecf0f1')
    
    app = SimpleFileOrganizerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
