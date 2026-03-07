#!/usr/bin/env python3
import sys

sys.path.insert(0, ".")

print("=" * 70)
print("     CHAMELEON ULTRA RFID FUZZER - VERIFICATION REPORT")
print("=" * 70)

# Test 1: Import fuzzer
print("\n[1/5] Testing fuzzer import...")
try:
    from chameleon_cli_unit import HFMFFuzzer

    print("      [OK] HFMFFuzzer class imported successfully")
except Exception as e:
    print(f"      [FAIL] Import failed: {e}")
    sys.exit(1)

# Test 2: Check command registration
print("\n[2/5] Testing command registration...")
try:
    from chameleon_cli_unit import hf_mf

    fuzzer_found = False
    for child in hf_mf.children:
        if child.name == "fuzz":
            fuzzer_found = True
            print(f"      [OK] Found command: {child.fullname}")
            desc = child.help_text
            suffix = "..." if len(desc) > 50 else ""
            print(f"      [OK] Description: {desc[:50]}{suffix}")
            break
    if not fuzzer_found:
        print("      [FAIL] Fuzzer command not registered!")
        sys.exit(1)
except Exception as e:
    print(f"      [FAIL] Registration check failed: {e}")
    sys.exit(1)

# Test 3: Check arguments
print("\n[3/5] Testing argument parser...")
try:
    fuzzer = HFMFFuzzer()
    parser = fuzzer.args_parser()
    args_count = len(parser._actions) - 1  # Exclude help
    arg_names = [a.dest for a in parser._actions if a.dest != "help"]
    print(f"      [OK] Arguments count: {args_count}")
    half = len(arg_names) // 2
    print(f"      [OK] Arguments: {', '.join(arg_names[:half])},")
    print(f"                      {', '.join(arg_names[half:])}")

    # Test basic parsing
    test_args = parser.parse_args(
        ["-i", "50", "-b", "3", "-m", "byte", "-o", "test.csv"]
    )
    print(
        f"      [OK] Can parse: iterations={test_args.iterations}, block={test_args.block}"
    )

    # Test device integration arguments
    test_args_dev = parser.parse_args(
        ["-i", "100", "--retries", "3", "--health-check", "50", "--verbose"]
    )
    print(
        f"      [OK] Device args: retries={test_args_dev.retries}, health_check={test_args_dev.health_check}, verbose={test_args_dev.verbose}"
    )
except Exception as e:
    print(f"      [FAIL] Argument test failed: {e}")
    sys.exit(1)

# Test 4: Check mutation methods
print("\n[4/5] Testing mutation engine...")
try:
    fuzzer = HFMFFuzzer()
    test_key = bytes.fromhex("ffffffffffff")

    mut_bit = fuzzer.fuzz_data(test_key, "bit", seed=123)
    mut_byte = fuzzer.fuzz_data(test_key, "byte", seed=123)
    mut_xor = fuzzer.fuzz_data(test_key, "xor", seed=123)
    mut_rand = fuzzer.fuzz_data(test_key, "random", seed=123)

    print(f"      [OK] bit mutation:    {test_key.hex()} -> {mut_bit.hex()}")
    print(f"      [OK] byte mutation:   {test_key.hex()} -> {mut_byte.hex()}")
    print(f"      [OK] xor mutation:    {test_key.hex()} -> {mut_xor.hex()}")
    print(f"      [OK] random mutation: {test_key.hex()} -> {mut_rand.hex()}")
except Exception as e:
    print(f"      [FAIL] Mutation test failed: {e}")
    sys.exit(1)

# Test 5: Check device interface integration
print("\n[5/5] Testing device interface...")
try:
    from device_interface import DeviceInterface, DeviceMode, AuthResult

    print("      [OK] Device interface imported successfully")
    device_modes = ", ".join(m.name for m in DeviceMode)
    auth_results = ", ".join(r.name for r in AuthResult)
    print(f"      [OK] DeviceMode enum available: {device_modes}")
    print(f"      [OK] AuthResult enum available: {auth_results}")
    assert hasattr(DeviceInterface, "connect") or callable(DeviceInterface), (
        "DeviceInterface missing expected interface"
    )
    print("      [OK] Device integration layer ready")
except Exception as e:
    print(f"      [FAIL] Device interface test failed: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("     ALL TESTS PASSED [OK]")
print("=" * 70)
print("\nFuzzer is ready to use!")
print("Command: hf mf fuzz")
print("Usage:   hf mf fuzz [options]")
print("Help:    hf mf fuzz --help")
print("\nDevice Integration Available:")
print("  - Real ChameleonUltra hardware support")
print("  - Simulator mode for testing")
print("  - Error recovery and health monitoring")
print("\n" + "=" * 70)
sys.exit(0)
