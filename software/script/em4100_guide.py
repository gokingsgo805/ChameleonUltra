#!/usr/bin/env python3
"""
EM4100 Card Reading Guide

Your card has been identified as EM4100 (Low Frequency).

To read your card, use the CLI that's currently running.
"""

import sys

# Color codes
CR = '\033[91m'   # Red
CG = '\033[92m'   # Green
CY = '\033[93m'   # Yellow
CB = '\033[94m'   # Blue
CC = '\033[96m'   # Cyan
C0 = '\033[0m'    # Reset

def main():
    print(f"\n{CB}{'=' * 70}{C0}")
    print(f"{CB}         EM4100 CARD - READING INSTRUCTIONS{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")
    
    print(f"{CG}Your Card Info:{C0}")
    print(f"  Type:       EM4100 RFID Tag")
    print(f"  Frequency:  125 kHz (LF - Low Frequency)")
    print(f"  Common Use: Access cards, badges, animal tags\n")
    
    print(f"{CY}Step 1: In the CLI console, place your card on the antenna\n")
    
    print(f"{CY}Step 2: Type this command and press Enter:{C0}")
    print(f"  {CG}lf em 410x read{C0}\n")
    
    print(f"{CY}Expected Output:{C0}")
    print(f"  EM410x ID: xxxxxxxxxx")
    print(f"  (Your 10-digit hex card ID)\n")
    
    print(f"{CB}Other Useful Commands:{C0}")
    print(f"  {CG}lf em 410x clone{C0}   - Clone card to Chameleon")
    print(f"  {CG}lf em 410x sim{C0}     - Simulate/emulate the card")
    print(f"  {CG}lf em 410x write{C0}   - Write custom ID")
    print(f"  {CG}lf search{C0}          - Search for any LF card\n")
    
    print(f"{CB}More Advanced:{C0}")
    print(f"  {CG}help lf em 410x{C0}    - See all EM4100 options")
    print(f"  {CG}help{C0}               - List all available commands\n")
    
    print(f"{CG}{'=' * 70}{C0}")
    print(f"{CG}CLI Status: Running{C0}")
    print(f"{CG}Device: Waiting for commands...{C0}")
    print(f"{CG}{'=' * 70}{C0}\n")

if __name__ == "__main__":
    main()
