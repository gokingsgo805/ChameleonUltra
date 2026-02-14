#!/usr/bin/env python3
"""
Create T55xx Key Dictionary (.dic) files

T55xx uses 32-bit passwords (8 hex characters)
Unlike MIFARE Classic which uses 48-bit keys (12 hex characters)

Usage:
    python create_t55xx_dic.py              # Create default dictionary
    python create_t55xx_dic.py custom.dic   # Create with custom name
"""

import sys
import os

# Color codes
CR = '\033[91m'   # Red
CG = '\033[92m'   # Green
CY = '\033[93m'   # Yellow
CB = '\033[94m'   # Blue
CC = '\033[96m'   # Cyan
CM = '\033[95m'   # Magenta
C0 = '\033[0m'    # Reset

# Common T55xx passwords (32-bit = 8 hex chars)
COMMON_T55XX_PASSWORDS = [
    # Factory/Default
    "00000000",  # All zeros (most common factory default)
    "FFFFFFFF",  # All ones
    
    # Simple patterns
    "12345678",  # Sequential
    "87654321",  # Reverse sequential
    "11111111",  # All ones (decimal)
    "22222222",  # All twos
    "33333333",  # All threes
    "44444444",  # All fours
    "55555555",  # All fives
    "66666666",  # All sixes
    "77777777",  # All sevens
    "88888888",  # All eights
    "99999999",  # All nines
    "AAAAAAAA",  # All A's
    "BBBBBBBB",  # All B's
    
    # Common passwords
    "51243648",  # Known common password
    "19920427",  # Date format (1992-04-27)
    "20240101",  # Date format (2024-01-01)
    "A0A0A0A0",  # Pattern A
    "05F6FB5D",  # Another common
    "13371337",  # Leet speak
    
    # Alternating patterns
    "FF00FF00",  # Alternating FF/00
    "00FF00FF",  # Alternating 00/FF
    "AAAA5555",  # AAAA then 5555
    "5555AAAA",  # 5555 then AAAA
    
    # More patterns
    "01010101",  # 01 pattern
    "10101010",  # 10 pattern
    "F0F0F0F0",  # F0 pattern
    "0F0F0F0F",  # 0F pattern
]

def create_t55xx_dic(filename):
    """Create a T55xx dictionary file"""
    try:
        # Ensure absolute path
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
        
        with open(filename, 'w') as f:
            for password in COMMON_T55XX_PASSWORDS:
                f.write(password + '\n')
        
        return filename
    except IOError as e:
        print(f"{CR}✗ Error creating file: {e}{C0}")
        return None

def validate_t55xx_dic(filename):
    """Validate T55xx dictionary format"""
    if not os.path.exists(filename):
        print(f"{CR}✗ File not found: {filename}{C0}")
        return False
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        print(f"\n{CB}Validating {os.path.basename(filename)}...{C0}\n")
        
        valid_count = 0
        invalid_count = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # T55xx passwords are 32-bit = 8 hex characters
            if len(line) != 8:
                print(f"{CR}✗ Line {i}: Invalid length {len(line)} (expected 8): {line}{C0}")
                invalid_count += 1
                continue
            
            try:
                int(line, 16)
                print(f"{CG}✓ Line {i}: {line}{C0}")
                valid_count += 1
            except ValueError:
                print(f"{CR}✗ Line {i}: Invalid hex: {line}{C0}")
                invalid_count += 1
        
        print(f"\n{CB}Results:{C0}")
        print(f"  Valid passwords: {CG}{valid_count}{C0}")
        print(f"  Invalid:         {CR}{invalid_count}{C0}")
        print(f"  Total:           {valid_count + invalid_count}\n")
        
        return invalid_count == 0
    
    except IOError as e:
        print(f"{CR}✗ Error reading file: {e}{C0}")
        return False

def main():
    print(f"\n{CB}{'=' * 70}{C0}")
    print(f"{CB}       T55xx KEY DICTIONARY (.dic) CREATOR{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")
    
    # Determine output filename
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = "common_t55xx_passwords.dic"
    
    print(f"{CG}Creating {output_file}...{C0}")
    print(f"  Passwords: {len(COMMON_T55XX_PASSWORDS)}")
    print(f"  Format:    8 hex characters (32-bit)\n")
    
    # Create the file
    result_file = create_t55xx_dic(output_file)
    
    if result_file:
        print(f"{CG}✓ Successfully created: {os.path.basename(result_file)}{C0}\n")
        
        # Validate it
        if validate_t55xx_dic(result_file):
            print(f"{CB}{'=' * 70}{C0}")
            print(f"{CG}NEXT STEPS${C0}")
            print(f"{CB}{'=' * 70}{C0}\n")
            
            print(f"{CY}To test your EM4100/T55xx card:${C0}")
            print(f"  1. Place card on Chameleon antenna")
            print(f"  2. In CLI, type:")
            print(f"     {CG}lf t55xx chk --dic {os.path.basename(result_file)}${C0}")
            print(f"  3. Tool will test all passwords from dictionary\n")
            
            print(f"{CY}If password is found:${C0}")
            print(f"  • You can clone: {CG}lf t55xx clone --pwd <password>${C0}")
            print(f"  • Or read data:  {CG}lf t55xx read --pwd <password>${C0}\n")
            
            print(f"{CY}File location:${C0}")
            print(f"  {CG}{result_file}${C0}\n")
            
            print(f"{CB}{'=' * 70}{C0}\n")
            return 0
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
