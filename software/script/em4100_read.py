#!/usr/bin/env python3
"""
Read EM4100 LF Card - Extract card ID and details

Usage:
    python em4100_read.py
"""

import sys
from chameleon_com import ChameleonCom

# Color codes
CR = '\033[91m'   # Red
CG = '\033[92m'   # Green
CY = '\033[93m'   # Yellow
CB = '\033[94m'   # Blue
CC = '\033[96m'   # Cyan
C0 = '\033[0m'    # Reset

def read_em4100():
    """Read EM4100 card and display details"""
    print(f"\n{CB}{'=' * 70}{C0}")
    print(f"{CB}         EM4100 CARD READER{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")
    
    print(f"{CY}Place card on Chameleon antenna...{C0}\n")
    
    try:
        cmd = ChameleonCom()
        
        print(f"{CB}[*] Attempting to read EM4100 card...{C0}")
        print("    Waiting for card detection (5 seconds)...\n")
        
        # Execute the read command
        # This connects to the device and attempts to read
        response = cmd.send_cmd("lf em 410x read")
        
        if response:
            print(f"{CG}✓ Card Read Successfully!{C0}\n")
            print(f"{CB}Card Details:{C0}")
            print(response)
        else:
            print(f"{CY}[*] Command sent, check CLI output for results{C0}\n")
            print(f"{CY}If CLI shows card data above, read was successful{C0}\n")
            
    except Exception as e:
        print(f"{CR}✗ Error: {e}{C0}\n")
        print(f"{CY}Alternative: Use CLI command directly:{C0}")
        print(f"  In the CLI prompt, type: {CG}lf em 410x read{C0}\n")
        return 1
    
    print(f"\n{CG}{'=' * 70}{C0}")
    print(f"{CG}Other EM4100 Commands:{C0}")
    print(f"  {CG}lf em 410x clone{C0}  - Clone this card to device")
    print(f"  {CG}lf em 410x write{C0}  - Write custom ID to card")
    print(f"  {CG}lf em 410x sim{C0}    - Simulate card")
    print(f"{CG}{'=' * 70}{C0}\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(read_em4100())
