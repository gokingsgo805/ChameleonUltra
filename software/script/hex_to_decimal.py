#!/usr/bin/env python3
"""EM4100 card ID converter (hex -> decimal)."""

import sys

# Color codes
CR = "\033[91m"  # Red
CG = "\033[92m"  # Green
CY = "\033[93m"  # Yellow
CB = "\033[94m"  # Blue
C0 = "\033[0m"  # Reset


def hex_to_decimal(hex_string):
    """Convert a hex string to decimal, returning None on invalid input."""
    try:
        hex_clean = hex_string.replace(" ", "").replace("0x", "").replace("0X", "")
        if not hex_clean:
            return None
        return int(hex_clean, 16)
    except ValueError:
        return None


def analyze_card_id(hex_id):
    """Analyze and display card ID information. Returns True on success."""
    print(f"\n{CB}{'=' * 70}{C0}")
    print(f"{CB}         EM4100 CARD ID ANALYSIS{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")

    decimal = hex_to_decimal(hex_id)
    if decimal is None:
        print(f"{CR}[FAIL] Invalid hex format: {hex_id}{C0}")
        return False

    print(f"{CG}Card ID Information:{C0}")

    # EM4100 IDs are commonly represented as 5 bytes (10 hex chars).
    hex_clean = hex_id.replace(" ", "").replace("0x", "").replace("0X", "").upper()
    if len(hex_clean) % 2:
        hex_clean = "0" + hex_clean
    hex_padded = hex_clean.zfill(10)
    hex_grouped = " ".join(hex_padded[i : i + 2] for i in range(0, len(hex_padded), 2))
    print(f"  {CY}Hexadecimal:{C0}  {CG}{hex_padded}{C0}")
    print(f"  {CY}Hex (bytes):{C0}  {CG}{hex_grouped}{C0}")
    print(f"  {CY}Decimal:     {C0} {CG}{decimal}{C0}\n")

    bit_length = decimal.bit_length() if decimal > 0 else 1
    print(f"{CY}Technical Details:{C0}")
    print(f"  Bit Length:    {bit_length} bits")
    print(f"  Byte Length:   {(bit_length + 7) // 8} bytes")
    print(f"  Max Value:     {(1 << bit_length) - 1}\n")

    print(f"{CY}Alternative Formats:{C0}")
    print(f"  Binary:        {bin(decimal)[2:]}")
    print(f"  Octal:         {oct(decimal)[2:]}")
    print(f"  Hex (0x):      0x{decimal:X}\n")

    print(f"{CY}EM4100 Card Details:{C0}")
    print("  Manufacturer:  EM4100 (EM Microelectronic)")
    print("  Frequency:     125 kHz (LF)")
    print("  Format:        Read-Only Standard")
    print("  Typical Use:   Access control, Animal tagging, RFID badges\n")

    print(f"{CB}{'=' * 70}{C0}\n")

    return True


def example_conversions():
    """Show example hex-to-decimal conversions."""
    print(f"\n{CB}Common EM4100 Card Examples:{C0}")

    examples = [
        ("12345678", "Demo Card"),
        ("FFFFFFFF", "All Ones (Test)"),
        ("00000000", "All Zeros (Test)"),
        ("DEADBEEF", "Sample ID"),
    ]

    for hex_val, desc in examples:
        decimal = hex_to_decimal(hex_val)
        print(f"  {hex_val} -> {decimal:10d}  ({desc})")

    print()


def main():
    """CLI entry point."""
    print(f"\n{CY}{'=' * 70}{C0}")
    print(f"{CY}          EM4100 HEX TO DECIMAL CONVERTER{C0}")
    print(f"{CY} WRITTEN/COMPILED/STAGED by @gokingsgo805{C0}")
    print(f"{CY}{'=' * 70}{C0}\n")

    if len(sys.argv) > 1:
        hex_id = sys.argv[1]
        ok = analyze_card_id(hex_id)
        return 0 if ok else 1
    print(f"{CY}Enter your card ID in hexadecimal format:{C0}")
    print(f"{CY}  Examples: 12345678, 0x12345678, FF FF FF FF{C0}\n")

    hex_input = input(f"{CG}Hex ID (or 'q' to quit): {C0}").strip()

    if hex_input.lower() == "q":
        print(f"{CY}Goodbye!{C0}\n")
        return 0

    if not hex_input:
        print(f"{CR}[FAIL] No input provided{C0}\n")
        return 1

    ok = analyze_card_id(hex_input)
    if not ok:
        return 1

    if input(f"{CG}Show example conversions? (y/n): {C0}").strip().lower() == "y":
        example_conversions()

    return 0


if __name__ == "__main__":
    sys.exit(main())
