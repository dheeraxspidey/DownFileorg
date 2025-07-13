#!/usr/bin/env python3
"""
Simple File Organizer GUI
Organizes files in Downloads folder automatically using AI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import shutil
from pathlib import Path
from random_forest_classifier import RandomForestFileClassifier

class SimpleFileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🗂️ Simple File Organizer")
        self.root.geometry("500x450")  # Made taller to fit all elements
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)  # Allow resizing so user can see all elements
        
        # Initialize classifier
        self.classifier = None
        self.load_classifier()
        
        # Default to Downloads folder
        self.downloads_path = str(Path.home() / "Downloads")
        
        # Create GUI
        self.create_widgets()
        
    def load_classifier(self):
        """Load the trained Random Forest classifier."""
        try:
            self.classifier = RandomForestFileClassifier()
            if os.path.exists('rf_file_classifier.joblib'):
                self.classifier.load_model('rf_file_classifier.joblib')
                print("✅ Classifier loaded successfully")
            else:
                messagebox.showerror("Error", "Model file not found. Please train the model first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classifier: {e}")
    
    def create_widgets(self):
        """Create simple GUI widgets."""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🗂️ File Organizer", 
            font=('Arial', 20, 'bold'),
            fg='white', 
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Instruction
        instruction_label = tk.Label(
            main_frame,
            text="Organize your Downloads folder automatically with AI",
            font=('Arial', 11),
            fg='#2c3e50',
            bg='#f0f0f0'
        )
        instruction_label.pack(pady=(0, 15))
        
        # Folder selection
        folder_frame = tk.LabelFrame(
            main_frame, 
            text="📁 Select Folder to Organize", 
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=15,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        folder_frame.pack(fill='x', pady=(0, 15))
        
        # Folder path display
        self.folder_var = tk.StringVar(value=self.downloads_path)
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
