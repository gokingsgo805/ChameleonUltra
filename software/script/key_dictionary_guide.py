#!/usr/bin/env python3
"""
Key Dictionary (.dic) Usage Guide

Key dictionaries are used to test multiple MIFARE Classic keys against a card.
NOT applicable to LF cards like EM4100 (which are read-only).

Usage:
    python key_dictionary_guide.py
"""
# Color codes
CR = "\033[91m"  # Red
CG = "\033[92m"  # Green
CY = "\033[93m"  # Yellow
CB = "\033[94m"  # Blue
CC = "\033[96m"  # Cyan
CM = "\033[95m"  # Magenta
C0 = "\033[0m"  # Reset


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{CB}{'=' * 70}{C0}")
    print(f"{CB}  {title}{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")


def main():
    print_section("KEY DICTIONARY (.dic) USAGE GUIDE")

    print(f"{CY}What are .dic files?{C0}")
    print("  Dictionary files containing MIFARE Classic keys (one per line)")
    print("  Format: One 12-character hex key per line")
    print("  Example content:")
    print(f"    {CG}FFFFFFFFFFFF{C0}  (Default key)")
    print(f"    {CG}000000000000{C0}  (All zeros)")
    print(f"    {CG}A0A1A2A3A4A5{C0}  (Common key)\n")

    print(f"{CY}IMPORTANT: Your Card Type{C0}")
    print(f"  Your card:{C0}  {CR}EM4100 (LF - Low Frequency){C0}")
    print(f"  .dic files:{C0} {CG}MIFARE Classic ONLY (HF - High Frequency){C0}")
    print(f"{CR}⚠ Key dictionaries DO NOT work with EM4100 cards!{C0}\n")

    print_section("✓ HOW TO USE .dic FILES (WITH MIFARE CLASSIC)")

    print(f"{CG}Step 1: Prepare a .dic file{C0}")
    print("  Create a file named: keys.dic")
    print("  Add keys (one per line):")
    print(f"    {CG}FFFFFFFFFFFF{C0}")
    print(f"    {CG}000000000000{C0}")
    print(f"    {CG}A0A1A2A3A4A5{C0}\n")

    print(f"{CG}Step 2: Test keys against MIFARE Classic card{C0}")
    print("  Command: hf mf fchk --dic keys.dic")
    print("  This will test each key in the dictionary\n")

    print(f"{CG}Step 3: Export found keys{C0}")
    print("  Command: hf mf fchk --dic keys.dic --export-key found.key")
    print("  This saves found keys to a .key file\n")

    print_section("EXAMPLE .dic FILE CREATION")

    print(f"{CG}Create common_keys.dic:{C0}\n")

    dic_content = """FFFFFFFFFFFF
000000000000
A0A1A2A3A4A5
B0B1B2B3B4B5
C0C1C2C3C4C5
D0D1D2D3D4D5
AABBCCDDEEFF
123456789ABC
ABABABABCDCD
D2F2F2F2F2F2
"""

    print(dic_content)

    print(f"{CG}Save to file and use:{C0}")
    print("  python em4100_create_dic.py > common_keys.dic")
    print("  Then in CLI: hf mf fchk --dic common_keys.dic\n")

    print_section("KEY TYPES FOR MIFARE CLASSIC")

    print(f"{CG}MIFARE Classic has two key types per sector:{C0}")
    print("  • Key A:  Used to read and write (0x60)")
    print("  • Key B:  Used to read and modify access bits (0x61)\n")
    print("Keys are 6 bytes (48 bits) = 12 hex characters\n")

    print_section("CLI COMMANDS USING .dic FILES")

    print(f"{CG}Basic key checking:{C0}")
    print("  hf mf fchk --dic keys.dic\n")

    print(f"{CG}Check specific sectors only:{C0}")
    print("  hf mf fchk --dic keys.dic")
    print("  (Default: checks all 40 sectors for 4K card)\n")

    print(f"{CG}Export found keys:{C0}")
    print("  hf mf fchk --dic keys.dic --export-key found.key")
    print("  hf mf fchk --dic keys.dic --export-dic found.dic\n")

    print(f"{CG}Check 1K card only:{C0}")
    print("  hf mf fchk -1 --dic keys.dic\n")

    print(f"{CG}Check 4K card only:{C0}")
    print("  hf mf fchk -4 --dic keys.dic\n")

    print_section("YOUR CARD: EM4100 - ALTERNATIVE OPTIONS")

    print(f"{CY}Since your card is EM4100 (LF, Read-Only):{C0}")
    print("  ✓ You CAN read the card with: lf em 410x read")
    print("  ✓ You CAN clone it to Chameleon: lf em 410x clone")
    print("  ✓ You CAN simulate it: lf em 410x sim")
    print("  ✗ You CANNOT use .dic files (no keys to test)\n")

    print(f"{CY}If you want to test MIFARE Classic cards:{C0}")
    print("  1. Place a MIFARE Classic card (HF)")
    print("  2. Run: auto_detect_card.py (will detect HF type)")
    print("  3. Use: hf mf fchk --dic keys.dic\n")

    print_section("COMMON MIFARE CLASSIC KEYS")

    print(f"{CG}Default/Factory Keys:{C0}")
    print("  FFFFFFFFFFFF - MIFARE default (very common)")
    print("  000000000000 - All zeros")
    print("  A0A1A2A3A4A5 - Common custom key")
    print("  B0B1B2B3B4B5 - Another common key")
    print("  AABBCCDDEEFF - Hex pattern")
    print("  000102030405 - Sequential")
    print("  D3F7D3F7D3F7 - Infineon key")
    print("  5A5A5A5A5A5A - All A's in hex")
    print("  FFFFFFFFFFFF - All F's\n")

    print(f"{CB}{'=' * 70}{C0}")
    print(f"{CB}SUMMARY{C0}")
    print(f"{CB}{'=' * 70}{C0}")
    print(f"  Your Card Type:        {CG}EM4100 (LF - Read-Only){C0}")
    print(f"  Key Dictionary Use:    {CR}Not applicable{C0}")
    print(f"  Available Commands:    {CG}lf em 410x read/clone/sim{C0}")
    print(f"  For MIFARE (HF):       {CG}Use .dic files with hf mf fchk{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")


if __name__ == "__main__":
    main()
