#!/usr/bin/env python3
import sys

sys.path.insert(0, ".")
from chameleon_cli_unit import hf_mf

# Check if fuzz command is in the hf_mf command tree
for child in hf_mf.children:
    if child.name == "fuzz":
        print(f"✓ Found 'fuzz' command in hf_mf")
        print(f"  Full name: {child.fullname}")
        print(f"  Help text: {child.help_text}")
        unit_class = child.cls
        if unit_class:
            print(f"  Class: {unit_class.__name__}")
            parser = unit_class().args_parser()
            print(f"  Description: {parser.description}")
            print("\n  Arguments:")
            for action in parser._actions[1:]:  # Skip help
                if hasattr(action, "dest"):
                    print(f"    --{action.dest}: {action.help}")
        break
else:
    print("✗ 'fuzz' command not found")
    print("\nAvailable commands in hf_mf:")
    for child in hf_mf.children:
        print(f"  - {child.name}: {child.help_text}")
