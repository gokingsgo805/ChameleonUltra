#!/usr/bin/env python3
"""
EM4100 Card Reader - Hex to Decimal Converter

Reads EM4100 card IDs and displays them in both hex and decimal formats.

Usage:
    python hex_to_decimal.py <hex_id>
    # or run with no args for interactive prompt
"""

import sys

# Color codes
CR = "\033[91m"  # Red
CG = "\033[92m"  # Green
CY = "\033[93m"  # Yellow
CB = "\033[94m"  # Blue
CC = "\033[96m"  # Cyan
CM = "\033[95m"  # Magenta
C0 = "\033[0m"  # Reset


def hex_to_decimal(hex_string):
    """Convert hex string to decimal"""
    try:
        # Remove spaces and convert
        hex_clean = hex_string.replace(" ", "").replace("0x", "").replace("0X", "")
        if not hex_clean:
            return None
        decimal = int(hex_clean, 16)
        return decimal
    except ValueError:
        return None


def analyze_card_id(hex_id):
    """Analyze and display card ID information. Returns True on success."""
    print(f"\n{CB}{'=' * 70}{C0}")
    print(f"{CB}         EM4100 CARD ID ANALYSIS{C0}")
    print(f"{CB}{'=' * 70}{C0}\n")

    # Convert to decimal
    decimal = hex_to_decimal(hex_id)

    if decimal is None:
        print(f"{CR}✗ Invalid hex format: {hex_id}{C0}")
        return False

    print(f"{CG}Card ID Information:{C0}")
    # Clean and pretty-print (EM4100 is typically 5 bytes = 10 hex chars)
    hex_clean = hex_id.replace(" ", "").replace("0x", "").replace("0X", "").upper()
    if len(hex_clean) % 2:
        hex_clean = "0" + hex_clean

    # Pad to 10 chars for common EM4100 display (5 bytes)
    hex_padded = hex_clean.zfill(10)
    hex_grouped = " ".join(hex_padded[i : i + 2] for i in range(0, len(hex_padded), 2))

    print(f"  {CY}Hexadecimal:{C0}  {CG}{hex_padded}{C0}")
    print(f"  {CY}Hex (bytes):{C0}  {CG}{hex_grouped}{C0}")
    print(f"  {CY}Decimal:     {C0}  {CG}{decimal}{C0}\n")

    # Calculate bit length
    bit_length = decimal.bit_length()
    print(f"{CY}Technical Details:{C0}")
    print(f"  Bit Length:    {bit_length} bits")
    print(f"  Byte Length:   {(bit_length + 7) // 8} bytes")
    print(f"  Max Value:     {(1 << bit_length) - 1}\n")

    # Display in different formats
    print(f"{CY}Alternative Formats:{C0}")
    print(f"  Binary:        {bin(decimal)[2:].upper()}")
    print(f"  Octal:         {oct(decimal)[2:].upper()}")
    print(f"  Hex (0x):      {hex(decimal).upper()}\n")

    # EM4100 specific details
    print(f"{CY}EM4100 Card Details:{C0}")
    print(f"  Manufacturer:  EM4100 (EM Microelectronic)")
    print(f"  Frequency:     125 kHz (LF)")
    print(f"  Format:        Read-Only Standard")
    print(f"  Typical Use:   Access control, Animal tagging, RFID badges\n")

    print(f"{CB}{'=' * 70}{C0}\n")
    return True


def example_conversions():
    """Show example hex to decimal conversions"""
    print(f"\n{CB}Common EM4100 Card Examples:{C0}")

    examples = [
        ("12345678", "Demo Card"),
        ("FFFFFFFF", "All Ones (Test)"),
        ("00000000", "All Zeros (Test)"),
        ("DEADBEEF", "Sample ID"),
    ]

    for hex_val, desc in examples:
        decimal = hex_to_decimal(hex_val)
        print(f"  {hex_val} → {decimal:10d}  ({desc})")

    print()


def main():
    """Main function"""
    print(
        f"\n{CG}╔════════════════════════════════════════════════════════════════════╗{C0}"
    )
    print(
        f"{CG}║          EM4100 HEX TO DECIMAL CONVERTER                          ║{C0}"
    )
    print(
        f"{CG}╚════════════════════════════════════════════════════════════════════╝{C0}\n"
    )

    # Check for command line argument
    if len(sys.argv) > 1:
        hex_id = sys.argv[1]
        ok = analyze_card_id(hex_id)
        return 0 if ok else 1
    else:
        # Interactive mode
        print(f"{CY}Enter your card ID in hexadecimal format:{C0}")
        print(f"  Examples: 12345678, 0x12345678, FF FF FF FF\n")

        hex_input = input(f"{CG}Hex ID (or 'q' to quit): {C0}").strip()

        if hex_input.lower() == "q":
            print(f"{CY}Goodbye!{C0}\n")
            return 0

        if not hex_input:
            print(f"{CR}✗ No input provided{C0}\n")
            return 1

        ok = analyze_card_id(hex_input)
        if not ok:
            return 1

        # Show examples
        show_examples = (
            input(f"{CG}Show example conversions? (y/n): {C0}").strip().lower()
        )
        if show_examples == "y":
                example_conversions()

            return 0


if __name__ == "__main__":
    sys.exit(main())
