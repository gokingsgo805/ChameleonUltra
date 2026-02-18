#!/usr/bin/env python3
"""Create a test MIFARE Classic dump for nested attack testing"""

import os
import subprocess

test_dump = "test_card.dump"

# Create a 1K dump (64 blocks, 16 bytes each)
with open(test_dump, "wb") as f:
    for block in range(64):
        if block % 4 == 3:  # Trailer block
            f.write(bytes.fromhex("FFFFFFFFFFFF078069FFFFFFFFFFFF"))
        else:
            f.write(bytes.fromhex("0102030405060708090A0B0C0D0E0F10"))

print(f"Created: {test_dump} ({os.path.getsize(test_dump)} bytes)")
print("Running nested attack...\n")

# Run nested attack
result = subprocess.run(
    [r"C:\Temp\nested.exe", "--dump", test_dump],
    capture_output=True,
    text=True,
    timeout=60,
)

print(f"Exit code: {result.returncode}")
if result.stdout:
    print(f"Output:\n{result.stdout}")
if result.stderr:
    print(f"Stderr:\n{result.stderr}")
