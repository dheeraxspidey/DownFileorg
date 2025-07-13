#!/usr/bin/env python3
"""
Modern File Organizer GUI with Unique Dark Theme
AI-powered file organization with beautiful, modern interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
import shutil
from pathlib import Path
from random_forest_classifier import RandomForestFileClassifier

class ModernFileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ AI File Organizer Pro")
        self.root.geometry("700x600")
        
        # Modern dark theme colors
        self.colors = {
            'bg_primary': '#0f0f0f',      # Deep black
            'bg_secondary': '#1a1a1a',    # Dark gray
            'bg_card': '#252525',         # Card background
            'accent_purple': '#8b5cf6',   # Purple accent
            'accent_blue': '#3b82f6',     # Blue accent
            'accent_green': '#10b981',    # Green accent
            'text_primary': '#ffffff',    # White text
            'text_secondary': '#a1a1aa',  # Gray text
            'text_muted': '#71717a',      # Muted text
            'border': '#404040',          # Border color
            'hover': '#2a2a2a',           # Hover state
            'error': '#ef4444',           # Error red
            'warning': '#f59e0b',         # Warning orange
        }
        
        # Configure main window
        self.root.configure(bg=self.colors['bg_primary'])
        self.root.resizable(True, True)
        self.root.minsize(650, 550)
        
        # Initialize classifier
        self.classifier = None
        self.animation_running = False
        self.load_classifier()
        
        # Default to Downloads folder
        self.downloads_path = str(Path.home() / "Downloads")
        
        # Setup modern styling
        self.setup_styles()
        
        # Create modern GUI
        self.create_modern_widgets()
        
        # Add window effects
        self.add_window_effects()
        
    def setup_styles(self):
        """Setup modern ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure progressbar
        style.configure(
            'Modern.Horizontal.TProgressbar',
            background=self.colors['accent_purple'],
            troughcolor=self.colors['bg_card'],
            borderwidth=0,
            lightcolor=self.colors['accent_purple'],
            darkcolor=self.colors['accent_purple']
        )
        
        # Configure buttons
        style.configure(
            'Modern.TButton',
            background=self.colors['bg_card'],
            foreground=self.colors['text_primary'],
            borderwidth=0,
            focuscolor='none'
        )
        
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
        """Create modern, beautiful widgets."""
        
        # Main container with padding
        main_container = tk.Frame(
            self.root, 
            bg=self.colors['bg_primary'],
            padx=30,
            pady=30
        )
        main_container.pack(fill='both', expand=True)
        
        # Header section
        self.create_header(main_container)
        
        # Spacer
        tk.Frame(main_container, bg=self.colors['bg_primary'], height=20).pack()
        
        # Stats card
        self.create_stats_card(main_container)
        
        # Spacer
        tk.Frame(main_container, bg=self.colors['bg_primary'], height=20).pack()
        
        # Folder selection card
        self.create_folder_card(main_container)
        
        # Spacer
        tk.Frame(main_container, bg=self.colors['bg_primary'], height=25).pack()
        
        # Progress section
        self.create_progress_section(main_container)
        
        # Spacer
        tk.Frame(main_container, bg=self.colors['bg_primary'], height=25).pack()
        
        # Action button
        self.create_action_button(main_container)
        
        # Footer
        tk.Frame(main_container, bg=self.colors['bg_primary'], height=20).pack()
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Create modern header with gradient-like effect."""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x')
        
        # Main title with gradient effect using multiple labels
        title_container = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_container.pack()
        
        # Icon and title
        icon_label = tk.Label(
            title_container,
            text="⚡",
            font=('Segoe UI', 32, 'bold'),
            fg=self.colors['accent_purple'],
            bg=self.colors['bg_primary']
        )
        icon_label.pack(side='left', padx=(0, 10))
        
        title_label = tk.Label(
            title_container,
            text="AI File Organizer Pro",
            font=('Segoe UI', 28, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_primary']
        )
        title_label.pack(side='left')
        
        # Subtitle
        subtitle = tk.Label(
            header_frame,
            text="Intelligent file organization powered by machine learning",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        subtitle.pack(pady=(5, 0))
    
    def create_stats_card(self, parent):
        """Create stats card with modern styling."""
        card_frame = tk.Frame(
            parent,
            bg=self.colors['bg_card'],
            relief='flat',
            bd=0
        )
        card_frame.pack(fill='x', pady=(0, 10))
        
        # Add subtle border effect
        border_frame = tk.Frame(card_frame, bg=self.colors['border'], height=1)
        border_frame.pack(fill='x', side='bottom')
        
        # Content
        content_frame = tk.Frame(card_frame, bg=self.colors['bg_card'], padx=25, pady=20)
        content_frame.pack(fill='x')
        
        # Stats grid
        stats_container = tk.Frame(content_frame, bg=self.colors['bg_card'])
        stats_container.pack(fill='x')
        
        # Files count
        files_frame = tk.Frame(stats_container, bg=self.colors['bg_card'])
        files_frame.pack(side='left', fill='x', expand=True)
        
        self.files_count_label = tk.Label(
            files_frame,
            text="0",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['accent_blue'],
            bg=self.colors['bg_card']
        )
        self.files_count_label.pack()
        
        tk.Label(
            files_frame,
            text="Files detected",
            font=('Segoe UI', 10),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_card']
        ).pack()
        
        # AI Status
        ai_frame = tk.Frame(stats_container, bg=self.colors['bg_card'])
        ai_frame.pack(side='right', fill='x', expand=True)
        
        ai_status = "🤖 AI Ready" if self.classifier else "❌ AI Error"
        ai_color = self.colors['accent_green'] if self.classifier else self.colors['error']
        
        tk.Label(
            ai_frame,
            text=ai_status,
            font=('Segoe UI', 12, 'bold'),
            fg=ai_color,
            bg=self.colors['bg_card']
        ).pack()
        
        tk.Label(
            ai_frame,
            text="Machine Learning Status",
            font=('Segoe UI', 10),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_card']
        ).pack()
    
    def create_folder_card(self, parent):
        """Create folder selection card."""
        card_frame = tk.Frame(
            parent,
            bg=self.colors['bg_card'],
            relief='flat',
            bd=0
        )
        card_frame.pack(fill='x')
        
        # Border effect
        tk.Frame(card_frame, bg=self.colors['border'], height=1).pack(fill='x', side='bottom')
        
        content_frame = tk.Frame(card_frame, bg=self.colors['bg_card'], padx=25, pady=25)
        content_frame.pack(fill='x')
        
        # Header
        tk.Label(
            content_frame,
            text="📁 Select Target Folder",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        ).pack(anchor='w', pady=(0, 15))
        
        # Folder selection row
        folder_row = tk.Frame(content_frame, bg=self.colors['bg_card'])
        folder_row.pack(fill='x')
        
        # Custom folder display
        self.folder_var = tk.StringVar(value=self.downloads_path)
        folder_display = tk.Frame(
            folder_row,
            bg=self.colors['bg_secondary'],
            relief='flat',
            bd=0
        )
        folder_display.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        # Folder path
        folder_label = tk.Label(
            folder_display,
            textvariable=self.folder_var,
            font=('Segoe UI', 10),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            anchor='w',
            padx=15,
            pady=12
        )
        folder_label.pack(fill='x')
        
        # Browse button with modern styling
        self.browse_btn = tk.Button(
            folder_row,
            text="Browse",
            command=self.browse_folder,
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['accent_purple'],
            activebackground=self.colors['hover'],
            activeforeground=self.colors['text_primary'],
            relief='flat',
            bd=0,
            padx=25,
            pady=12,
            cursor='hand2'
        )
        self.browse_btn.pack(side='right')
        
        # Add hover effects
        self.add_hover_effect(self.browse_btn, self.colors['accent_purple'], '#9333ea')
    
    def create_progress_section(self, parent):
        """Create modern progress section."""
        progress_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        progress_frame.pack(fill='x')
        
        # Progress bar with custom styling
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            style='Modern.Horizontal.TProgressbar',
            length=400
        )
        self.progress.pack(fill='x')
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to organize files",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        self.status_label.pack(pady=(15, 0))
    
    def create_action_button(self, parent):
        """Create the main action button with modern styling."""
        button_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        button_container.pack(fill='x')
        
        self.organize_btn = tk.Button(
            button_container,
            text="🚀 Organize Files with AI",
            command=self.organize_files,
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['accent_green'],
            activebackground='#059669',
            activeforeground=self.colors['text_primary'],
            relief='flat',
            bd=0,
            pady=18,
            cursor='hand2'
        )
        self.organize_btn.pack(fill='x', ipady=5)
        
        # Add hover effect
        self.add_hover_effect(self.organize_btn, self.colors['accent_green'], '#059669')
    
    def create_footer(self, parent):
        """Create footer with additional info."""
        footer_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        footer_frame.pack(fill='x')
        
        # Version info
        tk.Label(
            footer_frame,
            text="v2.0 • Built with AI • Modern Interface",
            font=('Segoe UI', 9),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_primary']
        ).pack()
    
    def add_hover_effect(self, widget, normal_color, hover_color):
        """Add hover effect to buttons."""
        def on_enter(e):
            widget.configure(bg=hover_color)
        
        def on_leave(e):
            widget.configure(bg=normal_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def add_window_effects(self):
        """Add modern window effects."""
        # Try to make window slightly transparent (Windows 10/11)
        try:
            self.root.wm_attributes('-alpha', 0.98)
        except:
            pass
    
    def browse_folder(self):
        """Browse for a folder to organize."""
        folder = filedialog.askdirectory(
            title="Select folder to organize",
            initialdir=self.downloads_path
        )
        if folder:
            self.folder_var.set(folder)
            self.downloads_path = folder
            self.update_file_count()
    
    def update_file_count(self):
        """Update the file count display."""
        count = self.count_files()
        self.files_count_label.config(text=str(count))
        
        # Add color coding based on file count
        if count == 0:
            color = self.colors['text_muted']
        elif count < 10:
            color = self.colors['accent_blue']
        elif count < 50:
            color = self.colors['accent_green']
        else:
            color = self.colors['warning']
        
        self.files_count_label.config(fg=color)
    
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
            messagebox.showerror("Error", "AI Classifier not loaded!")
            return
        
        if not os.path.exists(self.downloads_path):
            messagebox.showerror("Error", "Selected folder does not exist!")
            return
        
        # Update button state
        self.organize_btn.config(
            state='disabled', 
            text="🤖 AI Working...", 
            bg=self.colors['text_muted']
        )
        self.progress.start(10)
        self.status_label.config(text="🔍 Scanning files...", fg=self.colors['accent_blue'])
        
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
                self.root.after(0, lambda: self._show_completion("No files to organize!", 'info'))
                return
            
            # Create organized folders
            organized_count = 0
            categories = set()
            
            for i, file_path in enumerate(files):
                try:
                    # Update status
                    filename = os.path.basename(file_path)
                    display_name = filename[:25] + "..." if len(filename) > 25 else filename
                    self.root.after(0, lambda name=display_name: 
                                   self.status_label.config(
                                       text=f"🤖 Processing: {name}",
                                       fg=self.colors['accent_purple']
                                   ))
                    
                    # Classify file
                    result = self.classifier.predict(file_path)
                    category = result['folder_name']  # Use folder_name instead of predicted_category
                    categories.add(category)
                    
                    # Create category folder if it doesn't exist
                    category_folder = os.path.join(self.downloads_path, category)
                    os.makedirs(category_folder, exist_ok=True)
                    
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
            message = f"🎉 Successfully organized {organized_count} files into {len(categories)} categories:\n\n"
            message += " • " + "\n • ".join(sorted(categories))
            
            self.root.after(0, lambda: self._show_completion(message, 'success'))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_completion(f"❌ Error: {e}", 'error'))
    
    def _show_completion(self, message, msg_type='info'):
        """Show completion message and reset UI."""
        self.progress.stop()
        self.organize_btn.config(
            state='normal', 
            text="🚀 Organize Files with AI", 
            bg=self.colors['accent_green']
        )
        self.status_label.config(text="Ready to organize files", fg=self.colors['text_secondary'])
        self.update_file_count()
        
        # Show appropriate message box
        if msg_type == 'success':
            messagebox.showinfo("✨ Organization Complete", message)
        elif msg_type == 'error':
            messagebox.showerror("❌ Error", message)
        else:
            messagebox.showinfo("ℹ️ Information", message)


def main():
    """Main function to run the modern GUI."""
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        # You can add an icon file here
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    app = ModernFileOrganizerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
