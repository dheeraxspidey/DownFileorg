#!/usr/bin/env python3
"""
Automatic File Organizer with Watchdog
Monitors Downloads folder and automatically organizes files into categories.
"""

import os
import sys
import time
import shutil
import logging
from pathlib import Path
from typing import Dict, Set, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from random_forest_classifier import RandomForestFileClassifier

class FileOrganizerHandler(FileSystemEventHandler):
    """Handles file system events for automatic organization."""
    
    def __init__(self, downloads_path: str, classifier_model_path: str = "rf_file_classifier.joblib"):
        """
        Initialize the file organizer handler.
        
        Args:
            downloads_path: Path to Downloads folder to monitor
            classifier_model_path: Path to trained classifier model
        """
        self.downloads_path = Path(downloads_path)
        self.classifier = RandomForestFileClassifier()
        self.existing_folders: Set[str] = set()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('file_organizer.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load classifier
        try:
            if os.path.exists(classifier_model_path):
                self.classifier.load_model(classifier_model_path)
                self.logger.info(f"✅ Classifier loaded from {classifier_model_path}")
            else:
                self.logger.error(f"❌ Model file not found: {classifier_model_path}")
                raise FileNotFoundError(f"Model file not found: {classifier_model_path}")
        except Exception as e:
            self.logger.error(f"❌ Failed to load classifier: {e}")
            raise
        
        # Scan for existing folders
        self._scan_existing_folders()
        
        # Files to ignore (temporary, system files, etc.)
        self.ignore_patterns = {
            '.tmp', '.temp', '.crdownload', '.part', '.downloading',
            '.DS_Store', 'Thumbs.db', '.gitkeep', '.placeholder'
        }
        
        # Minimum file size to process (avoid processing incomplete downloads)
        self.min_file_size = 1024  # 1KB
        
        self.logger.info(f"🎯 File Organizer initialized for: {self.downloads_path}")
        self.logger.info(f"📁 Found existing folders: {', '.join(sorted(self.existing_folders))}")
    
    def _scan_existing_folders(self):
        """Scan Downloads folder for existing category folders."""
        if not self.downloads_path.exists():
            self.logger.warning(f"Downloads path does not exist: {self.downloads_path}")
            return
        
        for item in self.downloads_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                self.existing_folders.add(item.name)
                self.logger.info(f"📂 Found existing folder: {item.name}")
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored."""
        # Check file extension
        if file_path.suffix.lower() in self.ignore_patterns:
            return True
        
        # Check filename
        if file_path.name in self.ignore_patterns:
            return True
        
        # Check if it's a directory
        if file_path.is_dir():
            return True
        
        # Check file size (avoid incomplete downloads)
        try:
            if file_path.stat().st_size < self.min_file_size:
                return True
        except OSError:
            return True
        
        return False
    
    def _get_or_create_folder(self, folder_name: str) -> Path:
        """Get existing folder or create new one if needed."""
        folder_path = self.downloads_path / folder_name
        
        # Check if exact folder exists
        if folder_path.exists():
            return folder_path
        
        # Check for similar existing folders (case-insensitive)
        for existing_folder in self.existing_folders:
            if existing_folder.lower() == folder_name.lower():
                existing_path = self.downloads_path / existing_folder
                self.logger.info(f"📁 Using existing folder: {existing_folder}")
                return existing_path
        
        # Check for partial matches (e.g., "Education" vs "Education and Finance")
        folder_name_lower = folder_name.lower()
        for existing_folder in self.existing_folders:
            existing_lower = existing_folder.lower()
            
            # If new folder name contains existing folder name or vice versa
            if (folder_name_lower in existing_lower or existing_lower in folder_name_lower):
                existing_path = self.downloads_path / existing_folder
                self.logger.info(f"📁 Using similar existing folder: {existing_folder} (for {folder_name})")
                return existing_path
        
        # Create new folder
        try:
            folder_path.mkdir(exist_ok=True)
            self.existing_folders.add(folder_name)
            self.logger.info(f"📁 Created new folder: {folder_name}")
            return folder_path
        except Exception as e:
            self.logger.error(f"❌ Failed to create folder {folder_name}: {e}")
            # Fallback to Downloads root
            return self.downloads_path
    
    def _organize_file(self, file_path: Path):
        """Organize a single file."""
        try:
            # Skip if file should be ignored
            if self._should_ignore_file(file_path):
                return
            
            self.logger.info(f"🔍 Processing file: {file_path.name}")
            
            # Get prediction from classifier
            result = self.classifier.predict(str(file_path))
            folder_name = result.get('folder_name', result['predicted_category'])
            confidence = result['confidence']
            
            self.logger.info(f"🎯 Predicted: {folder_name} (confidence: {confidence:.3f})")
            
            # Get or create target folder
            target_folder = self._get_or_create_folder(folder_name)
            target_path = target_folder / file_path.name
            
            # Handle filename conflicts
            counter = 1
            original_target = target_path
            while target_path.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_path = original_target.parent / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move file
            try:
                shutil.move(str(file_path), str(target_path))
                self.logger.info(f"✅ Moved {file_path.name} → {target_folder.name}/")
                
                # Log to separate success file for statistics
                with open('organized_files.log', 'a') as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{file_path.name},{folder_name},{confidence:.3f}\n")
                    
            except Exception as e:
                self.logger.error(f"❌ Failed to move {file_path.name}: {e}")
                
        except Exception as e:
            self.logger.error(f"❌ Error processing {file_path.name}: {e}")
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Wait a bit to ensure file is completely downloaded
        time.sleep(2)
        
        # Check if file still exists and is complete
        if not file_path.exists():
            return
        
        self.logger.info(f"📥 New file detected: {file_path.name}")
        self._organize_file(file_path)
    
    def on_moved(self, event):
        """Handle file move events (e.g., browser completing download)."""
        if event.is_directory:
            return
        
        file_path = Path(event.dest_path)
        
        # Some browsers move files when download completes
        if file_path.exists() and not any(pattern in file_path.name for pattern in self.ignore_patterns):
            self.logger.info(f"📦 File completed download: {file_path.name}")
            self._organize_file(file_path)


class AutoFileOrganizer:
    """Main class for automatic file organization."""
    
    def __init__(self, downloads_path: str = None, model_path: str = "rf_file_classifier.joblib"):
        """
        Initialize the auto file organizer.
        
        Args:
            downloads_path: Path to Downloads folder (default: ~/Downloads)
            model_path: Path to classifier model
        """
        # Use default Downloads folder if not specified
        if downloads_path is None:
            downloads_path = str(Path.home() / "Downloads")
        
        self.downloads_path = Path(downloads_path)
        self.model_path = model_path
        self.observer = None
        self.handler = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def organize_existing_files(self):
        """Organize files that are already in the Downloads folder."""
        self.logger.info("🧹 Organizing existing files...")
        
        if not self.downloads_path.exists():
            self.logger.error(f"Downloads folder does not exist: {self.downloads_path}")
            return
        
        organized_count = 0
        
        # Get all files in Downloads (excluding subdirectories)
        files = [f for f in self.downloads_path.iterdir() 
                if f.is_file() and not f.name.startswith('.')]
        
        if not files:
            self.logger.info("📂 No files to organize in Downloads folder")
            return
        
        self.logger.info(f"📋 Found {len(files)} files to organize")
        
        for file_path in files:
            try:
                self.handler._organize_file(file_path)
                organized_count += 1
            except Exception as e:
                self.logger.error(f"❌ Failed to organize {file_path.name}: {e}")
        
        self.logger.info(f"✅ Organized {organized_count} existing files")
    
    def start_monitoring(self, organize_existing: bool = True):
        """Start monitoring the Downloads folder."""
        try:
            # Create handler
            self.handler = FileOrganizerHandler(str(self.downloads_path), self.model_path)
            
            # Organize existing files if requested
            if organize_existing:
                self.organize_existing_files()
            
            # Setup file system observer
            self.observer = Observer()
            self.observer.schedule(self.handler, str(self.downloads_path), recursive=False)
            
            # Start monitoring
            self.observer.start()
            self.logger.info(f"👀 Started monitoring: {self.downloads_path}")
            self.logger.info("🚀 Auto File Organizer is running! Press Ctrl+C to stop.")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop_monitoring()
                
        except Exception as e:
            self.logger.error(f"❌ Failed to start monitoring: {e}")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring the Downloads folder."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.logger.info("🛑 Stopped monitoring Downloads folder")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automatic File Organizer with Watchdog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Monitor ~/Downloads with existing files organization
  %(prog)s --path /path/to/folder    # Monitor custom folder
  %(prog)s --no-existing             # Skip organizing existing files
  %(prog)s --model custom_model.pkl  # Use custom classifier model

The organizer will:
  1. Monitor the specified folder for new files
  2. Automatically classify and move files to appropriate folders
  3. Reuse existing folders when possible
  4. Log all activities to file_organizer.log
        """
    )
    
    parser.add_argument('--path', '-p', 
                       help='Path to folder to monitor (default: ~/Downloads)')
    parser.add_argument('--model', '-m', default='rf_file_classifier.joblib',
                       help='Path to classifier model file')
    parser.add_argument('--no-existing', action='store_true',
                       help='Skip organizing existing files')
    parser.add_argument('--test', action='store_true',
                       help='Test mode - organize existing files only (no monitoring)')
    
    args = parser.parse_args()
    
    try:
        # Initialize organizer
        organizer = AutoFileOrganizer(args.path, args.model)
        
        if args.test:
            # Test mode - just organize existing files
            organizer.handler = FileOrganizerHandler(str(organizer.downloads_path), args.model)
            organizer.organize_existing_files()
        else:
            # Normal mode - start monitoring
            organizer.start_monitoring(organize_existing=not args.no_existing)
            
    except KeyboardInterrupt:
        print("\n👋 Auto File Organizer stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
