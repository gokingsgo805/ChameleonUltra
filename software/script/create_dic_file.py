#!/usr/bin/env python3
"""
Create and manage key dictionary (.dic) files for MIFARE Classic testing

Usage:
    python create_dic_file.py              # Create default common_keys.dic
    python create_dic_file.py output.dic   # Create with custom name
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

# Common MIFARE Classic keys
COMMON_MIFARE_KEYS = [
    # Default/Factory keys
    "FFFFFFFFFFFF",  # MIFARE default (very common)
    "000000000000",  # All zeros
    
    # Common custom keys
    "A0A1A2A3A4A5",  # Infineon key
    "B0B1B2B3B4B5",  # Common variant
    "C0C1C2C3C4C5",  # Another key
    "D0D1D2D3D4D5",  # Another key
    "AABBCCDDEEFF",  # Hex pattern
    "123456789ABC",  # Sequential
    "ABABABABCDCD",  # Pattern
    "D3F7D3F7D3F7",  # Repeating pattern
    
    # Additional patterns
    "5A5A5A5A5A5A",  # Repeating A's
    "FF00FF00FF00",  # Alternating F/0
    "001122334455",  # Sequential pairs
    "AABBCCDDEEFF",  # Hex pairs
    "112233445566",  # Incrementing
    "2A2A2A2A2A2A",  # Another pattern
]

def create_dic_file(filename):
    """Create a .dic file with common MIFARE keys"""
    try:
        # Ensure we have the full path
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
        
        with open(filename, 'w') as f:
            for key in COMMON_MIFARE_KEYS:
                f.write(key + '\n')
        
        return True
    except IOError as e:
        print(f"{CR}✗ Error creating file: {e}{C0}")
        return False

def validate_dic_file(filename):
    """Validate a .dic file format"""
    if not os.path.exists(filename):
        print(f"{CR}✗ File not found: {filename}{C0}")
        return False
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        print(f"\n{CB}Validating {filename}...{C0}\n")
        
        valid_count = 0
        invalid_count = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if valid hex, 12 chars (6 bytes)
            if len(line) != 12:
                print(f"{CR}✗ Line {i}: Invalid length {len(line)} (expected 12): {line}{C0}")
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
        print(f"  Valid keys:   {CG}{valid_count}{C0}")
        print(f"  Invalid keys: {CR}{invalid_count}{C0}")
        print(f"  Total:        {valid_count + invalid_count}\n")
        
        return invalid_count == 0
    
    except IOError as e:
        print(f"{CR}✗ Error reading file: {e}{C0}")
        return False

def merge_dic_files(input_files, output_file):
    """Merge multiple .dic files"""
    try:
        unique_keys = set()
        
        for input_file in input_files:
            if not os.path.exists(input_file):
                print(f"{CY}⚠ Skipping: {input_file} (not found){C0}")
                continue
            
            with open(input_file, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line and len(line) == 12:
                        unique_keys.add(line.upper())
        
        with open(output_file, 'w') as f:
            for key in sorted(unique_keys):
                f.write(key + '\n')
        
        print(f"{CG}✓ Merged {len(unique_keys)} unique keys{C0}")
        print(f"  Output: {CG}{output_file}{C0}\n")
        return True
    
    except Exception as e:
        print(f"{CR}✗ Error merging files: {e}{C0}")
        return False

def main():
    print(f"\n{CB}{'=' * 70}{C0}")
    print(f"{CB}         MIFARE CLASSIC KEY DICTIONARY (.dic) CREATOR{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")
    
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = "common_mifare_keys.dic"
    
    # Create the dictionary file
    print(f"{CG}Creating {output_file}...{C0}")
    
    if create_dic_file(output_file):
        print(f"{CG}✓ Successfully created: {output_file}{C0}")
        print(f"  Keys added: {len(COMMON_MIFARE_KEYS)}\n")
        
        # Validate it
        if validate_dic_file(output_file):
            print(f"{CB}{'=' * 70}{C0}")
            print(f"{CG}NEXT STEPS{C0}")
            print(f"{CB}{'=' * 70}{C0}\n")
            
            print(f"{CY}Using with CLI (for MIFARE Classic only):{C0}")
            print(f"  1. In CLI, place a MIFARE Classic card")
            print(f"  2. Type: {CG}hf mf fchk --dic {output_file}{C0}")
            print(f"  3. To export found keys:")
            print(f"     {CG}hf mf fchk --dic {output_file} --export-key found.key{C0}")
            print(f"     {CG}hf mf fchk --dic {output_file} --export-dic found.dic{C0}\n")
            
            print(f"{CY}Using with Fuzzer:{C0}")
            print(f"  • Create mutation of keys for security testing")
            print(f"  • Use: {CG}hf mf fuzz --dic {output_file}{C0}\n")
            
            print(f"{CB}{'=' * 70}{C0}\n")
            
            return 0
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
