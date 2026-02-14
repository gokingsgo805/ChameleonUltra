#!/usr/bin/env python3
"""
ChameleonUltra Auto-Detection & Fuzzer Testing Guide

Automated workflow:
1. hw connect → Auto-detects your card
2. hf mf fuzz → Tests your card for vulnerabilities

Usage:
    python connect_and_test_guide.py
"""

# Color codes
CR = "\033[91m"  # Red
CG = "\033[92m"  # Green
CY = "\033[93m"  # Yellow
CB = "\033[94m"  # Blue
CC = "\033[96m"  # Cyan
CM = "\033[95m"  # Magenta
C0 = "\033[0m"  # Reset


def print_header():
    """Print header"""
    print(f"\n{CB}{'=' * 70}{C0}")
    print(f"{CB}   AUTOMATED CARD DETECTION & FUZZER TESTING WORKFLOW{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")


def main():
    print_header()

    print(f"{CG}STEP 1: Connect Device & Auto-Detect Card{C0}\n")

    print("In the CLI, type:")
    print(f"  {CG}hw connect{C0}\n")

    print("What happens:")
    print("  • Chameleon connects automatically")
    print(f"  • Card type is detected (EM4100, T55xx, MIFARE, etc)")
    print("  • Available commands are displayed")
    print("  • Device info and capabilities are shown\n")

    print(f"{CG}Expected output:{C0}")
    print(f"  [OK] Device searched")
    print(f"  [OK] Chameleon Ultra connected: v3.0")
    print(f"  [OK] Card Detected: EM4100 (LF - 125 kHz)")
    print(f"    Type: EM4100 RFID Tag")
    print(f"    Frequency: 125 kHz")
    print(f"  [OK] Available Commands")
    print(f"    - lf em 410x read")
    print(f"    - lf em 410x clone")
    print(f"    - lf t55xx chk\n")

    print(f"{CG}STEP 2: Test with Fuzzer{C0}\n")

    print(f"Once connected, test your card's robustness:")
    print(f"  {CG}hf mf fuzz{C0}              # Quick test (100 iterations)")
    print(f"  {CG}hf mf fuzz -i 500{C0}       # Medium test (500 iterations)")
    print(f"  {CG}hf mf fuzz -i 1000{C0}      # Comprehensive (1000 iterations)\n")

    print(f"{CG}STEP 3: Advanced Testing{C0}\n")

    print(f"Test different mutation strategies:")
    print(f"  {CG}hf mf fuzz -m bit{C0}        # Single bit flipping")
    print(f"  {CG}hf mf fuzz -m byte{C0}       # Entire byte replacement")
    print(f"  {CG}hf mf fuzz -m xor{C0}        # XOR operations")
    print(f"  {CG}hf mf fuzz -m random{C0}     # Random mutations\n")

    print(f"{CG}Test different sections:{C0}")
    print(f"  {CG}hf mf fuzz --block 0{C0}     # Block 0 (manufacturer)")
    print(f"  {CG}hf mf fuzz --block 3{C0}     # Block 3 (sector trailer)")
    print(f"  {CG}hf mf fuzz --target-type B{C0} # Key B instead of Key A\n")

    print(f"{CG}With device monitoring:{C0}")
    print(
        f"  {CG}hf mf fuzz --health-check 50{C0} # Health check every 50 iterations"
    )
    print(f"  {CG}hf mf fuzz --retries 3{C0}       # Retry on timeout\n")

    print(f"{CG}Save results:{C0}")
    print(f"  {CG}hf mf fuzz -o results.csv{C0}    # Export to CSV file\n")

    print(f"{CG}STEP 4: Full Real-World Test{C0}\n")

    print("Complete vulnerability assessment:")
    test_command = "hf mf fuzz -i 1000 -m byte --health-check 50 --retries 3 -o card_test.csv --verbose"
    print(f"  {CG}{test_command}{C0}\n")

    print("This will:")
    print("  • Run 1000 fuzzing iterations")
    print("  • Use byte mutation strategy")
    print("  • Check device health every 50 iterations")
    print("  • Retry on timeouts (3 retries max)")
    print("  • Save detailed results to card_test.csv")
    print("  • Show verbose output with device info\n")

    print(f"{CB}{'=' * 70}{C0}")
    print(f"{CB}COMMAND REFERENCE{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")

    print(f"{CY}Auto-Detection (on connect):{C0}")
    print(f"  lf search        - Manual card search")
    print(f"  lf em 410x info  - Get EM4100 details")
    print(f"  lf t55xx info    - Get T55xx details\n")

    print(f"{CY}EM4100 Operations:{C0}")
    print(f"  lf em 410x read  - Read card ID")
    print(f"  lf em 410x clone - Clone to Chameleon")
    print(f"  lf em 410x sim   - Simulate card\n")

    print(f"{CY}T55xx Operations:{C0}")
    print(f"  lf t55xx chk --dic common_t55xx_passwords.dic")
    print(f"  lf t55xx clone --pwd 00000000\n")

    print(f"{CY}Fuzzer Operations:{C0}")
    print(f"  hf mf fuzz -i <iterations>")
    print(f"  hf mf fuzz -m <mutation_type>  (bit, byte, xor, random)")
    print(f"  hf mf fuzz --block <block_num>")
    print(f"  hf mf fuzz --health-check <interval>\n")

    print(f"{CB}{'=' * 70}{C0}")
    print(f"{CB}TIPS FOR BEST RESULTS{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")

    print(f"[OK] Keep card on antenna during entire test")
    print(f"[OK] Use health checks for longer tests (--health-check 50)")
    print(f"[OK] Start with small iterations, increase gradually")
    print(f"[OK] Test multiple mutation strategies")
    print(f"[OK] Save results for documentation (--output file.csv)")
    print(f"[OK] Use verbose mode to see device details (--verbose)")
    print(f"[OK] Try T55xx password check before fuzzing")
    print(f"[OK] Monitor card temperature during extended testing\n")

    print(f"{CB}{'=' * 70}{C0}")
    print(f"{CG}QUICK START{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")

    print(f"1. {CG}hw connect{C0}")
    print(f"   -> Device connects, card auto-detected")
    print(f"2. {CG}hf mf fuzz -i 100 -m bit{C0}")
    print(f"   -> Run quick vulnerability test")
    print(f"3. {CG}hf mf fuzz -i 500 -o results.csv{C0}")
    print(f"   -> Run extended test, save results\n")

    print(f"{CB}{'=' * 70}{C0}\n")


if __name__ == "__main__":
    main()
