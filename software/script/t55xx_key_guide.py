#!/usr/bin/env python3
"""
T55xx Key Dictionary (.dic) Guide for EM4100 Tags

T55xx is the LF equivalent to MIFARE Classic - it uses keys for authentication.
EM4100 tags can emulate T55xx, so they can use T55xx key dictionaries.

Usage:
    python t55xx_key_guide.py
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
    print_section("T55xx KEY DICTIONARY (.dic) GUIDE FOR EM4100 TAGS")

    print(f"{CY}What is T55xx?{C0}")
    print("  • LF (Low Frequency) chip used in access cards")
    print("  • Operates at 125 kHz (same as EM4100)")
    print("  • Supports PASSWORD PROTECTION (like MIFARE has keys)")
    print("  • Can be cloned/emulated by ChameleonUltra\n")

    print(f"{CY}EM4100 vs T55xx relationship:{C0}")
    print("  EM4100:  Read-only LF tag (no keys needed)")
    print("  T55xx:   LF chip WITH password protection (needs T55xx dict)")
    print("  Connection: EM4100 can EMULATE T55xx with password\n")

    print_section("T55xx KEY DICTIONARY FORMAT")

    print(f"{CG}T55xx uses 32-bit (8 hex chars) passwords:{C0}")
    print("  Format:    8 hexadecimal characters")
    print("  Example:   51243648")
    print("  Compare:   MIFARE Classic = 12 hex chars (6 bytes)\n")

    print(f"{CG}Example .dic file for T55xx:{C0}")
    print("  00000000  (all zeros - default)")
    print("  FFFFFFFF  (all ones)")
    print("  51243648  (common password)")
    print("  19920427  (date format)")
    print("  12345678  (sequential)\n")

    print_section("HOW TO USE T55xx DICTIONARIES WITH YOUR EM4100")

    print(f"{CG}Step 1: Have your EM4100 card ready{C0}")
    print("  Place it on the Chameleon antenna\n")

    print(f"{CG}Step 2: Load the T55xx dictionary{C0}")
    print("  Command: lf t55xx chk --dic t55xx_keys.dic\n")

    print(f"{CG}Step 3: Test for known passwords{C0}")
    print("  The tool will try each password from the dictionary")
    print("  If a password works, it will be displayed\n")

    print(f"{CG}Step 4: Clone/Emulate with password{C0}")
    print("  Once you find the password:")
    print("  Command: lf t55xx clone --pwd <password>\n")

    print_section("T55xx CLI COMMANDS")

    print(f"{CG}Basic T55xx commands:{C0}")
    print("  lf t55xx info          - Get T55xx info")
    print("  lf t55xx read          - Read T55xx data")
    print("  lf t55xx chk           - Check passwords")
    print("  lf t55xx chk --dic X   - Check with dictionary\n")

    print(f"{CG}Using with dictionary:{C0}")
    print("  lf t55xx chk --dic t55xx_keys.dic")
    print("  lf t55xx chk --dic common_t55xx_passwords.dic\n")

    print(f"{CG}Clone/Write operations:{C0}")
    print("  lf t55xx clone --pwd <password>")
    print("  lf t55xx write --pwd <password> <data>\n")

    print(f"{CG}Detect/Recover password:{C0}")
    print("  lf t55xx detect")
    print("  lf t55xx dump")
    print("  lf t55xx recover\n")

    print_section("COMMON T55xx PASSWORDS")

    print(f"{CG}Default/Factory Passwords:{C0}")
    print("  00000000 - All zeros (factory default)")
    print("  FFFFFFFF - All ones")
    print("  12345678 - Sequential numbers")
    print("  51243648 - Common/Random")
    print("  19920427 - Date format")
    print("  20240101 - Another date")
    print("  A0A0A0A0 - Pattern repeated")
    print("  55555555 - All fives")
    print("  98765432 - Reverse sequence\n")

    print_section("YOUR EM4100 CARD - T55xx CAPABILITY")

    print(f"{CY}Your card: EM4100 (LF - 125 kHz){C0}")
    print(f"  Can it use T55xx dictionaries?  {CG}YES ✓{C0}\n")

    print(f"{CG}Scenario 1: EM4100 is protected with T55xx password{C0}")
    print("  • Use: lf t55xx chk --dic t55xx_keys.dic")
    print("  • This will try to find the password\n")

    print(f"{CG}Scenario 2: You want to clone WITH T55xx protection{C0}")
    print("  • Read original: lf em 410x read")
    print("  • Clone as T55xx: lf t55xx clone --pwd <newpassword>\n")

    print(f"{CG}Scenario 3: Regular EM4100 (no T55xx){C0}")
    print("  • Use: lf em 410x read / lf em 410x clone")
    print("  • T55xx dictionary NOT needed\n")

    print_section("KEY DIFFERENCE: EM4100 vs T55xx")

    print(f"  {CB}Feature          │ EM4100        │ T55xx{C0}")
    print(f"  {CB}─────────────────┼───────────────┼──────────────{C0}")
    print("  Read-only         │ Yes           │ No")
    print("  Has password      │ No (inherent) │ Yes")
    print("  Key dict needed   │ No            │ Yes (T55xx)")
    print("  Key size          │ N/A           │ 32-bit (8 hex)")
    print("  Commands          │ lf em 410x    │ lf t55xx\n")

    print_section("NEXT STEPS")

    print(f"{CG}To use T55xx dictionaries with your card:{C0}")
    print()

    print("1. First, determine your card type:")
    print(f"   Command: {CG}auto_detect_card.py{C0}")
    print(f"   Or:      {CG}lf search{C0}")
    print()

    print("2. If it shows T55xx protection:")
    print(f"   Command: {CG}lf t55xx chk --dic t55xx_keys.dic{C0}")
    print()

    print("3. If password is found:")
    print("   You can then clone/modify the card")
    print()

    print("4. Get a T55xx dictionary:")
    print(f"   Command: {CG}python create_t55xx_dic.py{C0}")
    print()

    print(f"{CB}{'=' * 70}{C0}")
    print(f"{CB}SUMMARY{C0}")
    print(f"{CB}{'=' * 70}{C0}")
    print(f"  Your Card:            {CG}EM4100 (LF - 125 kHz){C0}")
    print(f"  Can use T55xx dict:   {CG}YES ✓{C0}")
    print(f"  Dictionary format:    {CG}8 hex chars (32-bit passwords){C0}")
    print(f"  Example dict entry:   {CG}00000000{C0}")
    print(f"  CLI command:          {CG}lf t55xx chk --dic <file>{C0}")
    print(f"{CB}{'=' * 70}{C0}")
    print()


if __name__ == "__main__":
    main()
