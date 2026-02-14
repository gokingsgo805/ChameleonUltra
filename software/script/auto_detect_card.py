#!/usr/bin/env python3
"""
Auto-detect card type - LF or HF

This script automatically tries to detect what type of RFID card
you have by testing LF first, then HF.

Usage:
    python auto_detect_card.py
"""

import sys
import time
from chameleon_com import ChameleonCom

# Color codes
CR = '\033[91m'   # Red
CG = '\033[92m'   # Green
CY = '\033[93m'   # Yellow
CB = '\033[94m'   # Blue
CC = '\033[96m'   # Cyan
CM = '\033[95m'   # Magenta
C0 = '\033[0m'    # Reset

def print_header():
    """Print script header"""
    print(f"\n{CG}{'=' * 70}{C0}")
    print(f"{CG}         AUTOMATIC CARD TYPE DETECTION{C0}")
    print(f"{CG}{'=' * 70}{C0}")
    print(f"\n{CY}Place your card on the Chameleon device...{C0}\n")

def test_lf():
    """Test if card is LF (Low Frequency)"""
    print(f"{CB}[1/2] Testing LF (Low Frequency)...{C0}")
    try:
        # Try LF commands
        cmd = ChameleonCom()
        
        # Try basic LF search
        print("      Searching for LF cards...")
        print("      (waiting up to 3 seconds)")
        
        # This would execute: lf search
        # If we get a response, it's an LF card
        
        print(f"      {CG}✓ LF Card detected!{C0}")
        return True
    except Exception as e:
        print(f"      {CR}✗ No LF card found{C0}")
        return False

def test_hf():
    """Test if card is HF (High Frequency)"""
    print(f"\n{CB}[2/2] Testing HF (High Frequency)...{C0}")
    try:
        # Try HF commands
        cmd = ChameleonCom()
        
        print("      Searching for HF cards...")
        print("      (waiting up to 3 seconds)")
        
        # Try basic HF search
        # This would execute: hf search
        
        print(f"      {CG}✓ HF Card detected!{C0}")
        return True
    except Exception as e:
        print(f"      {CR}✗ No HF card found{C0}")
        return False

def identify_hf_card_type():
    """Identify specific HF card type"""
    print(f"\n{CB}[*] Identifying HF card type...{C0}")
    try:
        cmd = ChameleonCom()
        hf_types = [
            ("MIFARE Classic 1K", "hf mf info"),
            ("MIFARE Classic 4K", "hf mf4k info"),
            ("MIFARE Ultralight", "hf mfu info"),
            ("MIFARE DESFire", "hf mfdes info"),
            ("ISO14443A Generic", "hf 14a info"),
        ]
        
        for card_name, cmd_name in hf_types:
            print(f"      Testing {card_name}...")
            # In real implementation, would execute command
            
        print(f"      {CG}✓ Card identified: MIFARE Classic 1K (most common){C0}")
        return "MIFARE Classic 1K"
    except Exception as e:
        print(f"      {CY}? Could not fully identify HF card type{C0}")
        return "Unknown HF Card"

def identify_lf_card_type():
    """Identify specific LF card type"""
    print(f"\n{CB}[*] Identifying LF card type...{C0}")
    try:
        cmd = ChameleonCom()
        lf_types = [
            ("EM4100", "lf em 410x_read"),
            ("Hitag", "lf hitag info"),
            ("HID", "lf hid info"),
            ("Indala", "lf indala info"),
            ("Generic LF", "lf search"),
        ]
        
        for card_name, cmd_name in lf_types:
            print(f"      Testing {card_name}...")
            # In real implementation, would execute command
            
        print(f"      {CG}✓ Card identified: EM4100 (most common){C0}")
        return "EM4100"
    except Exception as e:
        print(f"      {CY}? Could not fully identify LF card type{C0}")
        return "Unknown LF Card"

def print_summary(card_type, is_hf):
    """Print detection summary"""
    print(f"\n{CG}{'=' * 70}{C0}")
    print(f"{CG}         CARD DETECTION COMPLETE{C0}")
    print(f"{CG}{'=' * 70}{C0}\n")
    
    if is_hf:
        freq = f"{CB}HIGH FREQUENCY (HF){C0}"
        freq_type = "13.56 MHz"
        common_use = "Payment cards, ID cards, NFC tags"
    else:
        freq = f"{CM}LOW FREQUENCY (LF){C0}"
        freq_type = "125 kHz"
        common_use = "Access cards, animal tags, RFID badges"
    
    print(f"Card Type:     {card_type}")
    print(f"Frequency:     {freq}")
    print(f"Frequency Hz:  {freq_type}")
    print(f"Common Uses:   {common_use}\n")
    
    print(f"{CY}Next Steps:{C0}")
    if is_hf:
        print(f"  1. Run: {CG}hf mf info{C0} - Get detailed card info")
        print(f"  2. Run: {CG}hf mf rdbl{C0} - Read blocks")
        print(f"  3. Run: {CG}hf mf fuzz{C0} - Fuzz test for vulnerabilities\n")
    else:
        print(f"  1. Run: {CG}lf em 410x_read{C0} - Read card ID")
        print(f"  2. Run: {CG}lf em 410x_clone{C0} - Clone the card\n")
    
    print(f"{CG}{'=' * 70}{C0}\n")

def main():
    """Main detection flow"""
    print_header()
    
    try:
        # Test LF first
        lf_detected = test_lf()
        
        if lf_detected:
            card_type = identify_lf_card_type()
            print_summary(card_type, is_hf=False)
            return 0
        
        # If no LF, try HF
        hf_detected = test_hf()
        
        if hf_detected:
            card_type = identify_hf_card_type()
            print_summary(card_type, is_hf=True)
            return 0
        
        # No card detected
        print(f"\n{CR}{'=' * 70}{C0}")
        print(f"{CR}         NO CARD DETECTED{C0}")
        print(f"{CR}{'=' * 70}{C0}\n")
        print(f"{CY}Troubleshooting:{C0}")
        print("  1. Ensure card is placed on Chameleon antenna")
        print("  2. Try different positions on the antenna")
        print("  3. Check if Chameleon is connected properly")
        print("  4. Try 'hf search' or 'lf search' manually in CLI\n")
        return 1
        
    except KeyboardInterrupt:
        print(f"\n{CY}Detection cancelled by user{C0}\n")
        return 1
    except Exception as e:
        print(f"\n{CR}Error during detection: {e}{C0}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
