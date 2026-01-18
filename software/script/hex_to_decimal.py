#!/usr/bin/env python3
"""
Convert hexadecimal to decimal
"""

import sys


def hex_to_decimal(hex_value):
    """
    Convert hexadecimal string to decimal integer

    :param hex_value: Hexadecimal string (with or without 0x prefix)
    :return: Decimal integer
    """
    try:
        # Remove whitespace and convert to lowercase
        hex_value = hex_value.strip().lower()

        # Remove 0x prefix if present
        if hex_value.startswith("0x"):
            hex_value = hex_value[2:]

        # Convert to decimal
        decimal = int(hex_value, 16)
        return decimal
    except ValueError as e:
        print(f"Error: Invalid hexadecimal value '{hex_value}'")
        raise


def main():
    if len(sys.argv) > 1:
        # Take hex value from command line argument
        hex_value = sys.argv[1]
        try:
            decimal = hex_to_decimal(hex_value)
            print(f"Hexadecimal: {hex_value}")
            print(f"Decimal: {decimal}")
        except ValueError:
            sys.exit(1)
    else:
        # Interactive mode
        print("Hexadecimal to Decimal Converter")
        print("-" * 30)

        while True:
            try:
                hex_input = input(
                    "Enter hexadecimal value (or 'quit' to exit): "
                ).strip()

                if hex_input.lower() == "quit":
                    print("Goodbye!")
                    break

                if not hex_input:
                    print("Please enter a valid hexadecimal value")
                    continue

                decimal = hex_to_decimal(hex_input)
                print(f"Hexadecimal: {hex_input}")
                print(f"Decimal: {decimal}\n")

            except ValueError:
                print("Please try again.\n")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    main()
