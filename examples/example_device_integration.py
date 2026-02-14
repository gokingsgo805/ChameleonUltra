#!/usr/bin/env python3
"""
Device Integration Example - RFID Fuzzer with Real Hardware Support

This example demonstrates how to use the device integration layer
for fuzzing with ChameleonUltra hardware or simulator.

Usage:
    python example_device_integration.py                    # Use simulator
    python example_device_integration.py /dev/ttyUSB0       # Use real device
    python example_device_integration.py COM3               # Windows device
"""

import sys
from typing import Optional

# For standalone package
try:
    from chameleon_fuzzer import (
        RFIDFuzzer,
        DeviceInterface,
        MutationStrategy,
        KeyType,
        AuthResult,
    )
except ImportError:
    # For main repository
    sys.path.insert(0, 'software/script')
    from device_interface import DeviceInterface, AuthResult, KeyType


def example_basic_fuzzing():
    """Basic fuzzing example with simulator"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Fuzzing with Simulator")
    print("=" * 60)
    
    fuzzer = RFIDFuzzer(iterations=50)
    
    fuzzer.fuzz(
        original_key="FFFFFFFFFFFF",
        strategy=MutationStrategy.BIT,
        iterations=50,
        slowdown=0.01,
    )
    
    print(fuzzer.get_summary())


def example_device_detection(port: Optional[str] = None):
    """Device detection and validation example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Device Detection and Validation")
    print("=" * 60)
    
    if port:
        print(f"Attempting to detect device on {port}...")
    else:
        print("Using simulator mode (no real device)")
    
    device = DeviceInterface(port=port)
    
    # Start session - this detects and initializes device
    if device.start_session():
        print("✓ Device session started successfully")
        
        # Get device info
        if device.device_info:
            info = device.device_info
            print("\nDevice Information:")
            print(f"  Name: {info.name}")
            print(f"  Hardware: {info.hw_version}")
            print(f"  Firmware: {info.fw_version}")
            print(f"  Mode: {info.mode.value}")
            print(f"  Supports Reader Mode: {info.supports_reader_mode}")
            print(f"  Supports MIFARE Classic: {info.supports_mifare_classic}")
        
        device.end_session()
    else:
        print("✗ Failed to start device session")


def example_authentication_testing(port: Optional[str] = None):
    """Authentication testing with device"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Direct Authentication Testing")
    print("=" * 60)
    
    device = DeviceInterface(port=port)
    device.start_session()
    
    # Test different keys
    test_keys = [
        "FFFFFFFFFFFF",  # Factory default
        "000000000000",  # All zeros
        "AAAAAAAAAAAAA", # Pattern
    ]
    
    print("\nTesting authentication with different keys:")
    for key_hex in test_keys:
        key = bytes.fromhex(key_hex)
        result, error = device.test_authentication(
            block=0,
            key_type=KeyType.A,
            key=key,
            retry_count=1
        )
        
        status = "✓" if result == AuthResult.SUCCESS else "✗"
        print(f"  {status} Key {key_hex}: {result.value}")
        if error:
            print(f"      Error: {error}")
    
    device.end_session()


def example_session_statistics(port: Optional[str] = None):
    """Session statistics and monitoring example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Session Statistics and Monitoring")
    print("=" * 60)
    
    device = DeviceInterface(port=port)
    device.start_session()
    
    # Simulate some authentication attempts
    print("\nGenerating test data...")
    for i in range(20):
        key = bytes.fromhex("FFFFFFFFFFFF")
        device.test_authentication(0, KeyType.A, key, retry_count=1)
        if i % 5 == 4:
            # Check stats periodically
            stats = device.get_session_stats()
            elapsed = stats.get('elapsed_time', 0)
            success_rate = stats.get('success_rate', 0)
            throughput = stats.get('throughput', 0)
            print(f"  [{i+1}/20] Time: {elapsed:.2f}s, "
                  f"Success: {success_rate:.1f}%, "
                  f"Rate: {throughput:.2f} ops/sec")
    
    # Get final statistics
    print("\nFinal Statistics:")
    stats = device.get_session_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    device.end_session()


def example_fuzzing_with_device(port: Optional[str] = None):
    """Full fuzzing campaign with device"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Full Fuzzing Campaign with Device")
    print("=" * 60)
    
    device = DeviceInterface(port=port)
    fuzzer = RFIDFuzzer(iterations=100, device_interface=device)
    
    print("Starting fuzzing campaign...")
    print("  Strategy: XOR mutations")
    print("  Iterations: 100")
    print("  Retries: 3 on timeout")
    print("  Health check: Every 25 iterations")
    print()
    
    stats = fuzzer.fuzz(
        original_key="FFFFFFFFFFFF",
        strategy=MutationStrategy.XOR,
        iterations=100,
        slowdown=0.01,
        target_block=1,
        key_type=KeyType.A,
        retries=3,
        health_check_interval=25,
    )
    
    print(fuzzer.get_summary())
    
    # Show behavior distribution
    if stats.behavior_counts:
        print("\nBehavior Distribution:")
        total = sum(stats.behavior_counts.values())
        for behavior, count in sorted(
            stats.behavior_counts.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            percent = (count / total) * 100
            print(f"  {behavior}: {count} ({percent:.1f}%)")


def example_error_recovery(port: Optional[str] = None):
    """Error recovery and resilience example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Error Recovery and Resilience")
    print("=" * 60)
    
    device = DeviceInterface(port=port)
    device.start_session()
    
    print("Testing error recovery mechanisms...")
    
    # Test health check
    print("\n1. Device Health Check:")
    if device.validate_device_health():
        print("   ✓ Device is healthy")
    else:
        print("   ✗ Device health check failed")
    
    # Test connection recovery
    print("\n2. Connection Recovery:")
    if device.recover_connection():
        print("   ✓ Connection recovered")
    else:
        print("   ✗ Connection recovery failed")
    
    # Get session stats showing any errors
    print("\n3. Error Statistics:")
    stats = device.get_session_stats()
    error_count = stats.get('error_count', 0)
    timeout_count = stats.get('timeout_count', 0)
    print(f"   Errors: {error_count}")
    print(f"   Timeouts: {timeout_count}")
    
    device.end_session()


def example_export_results():
    """Export fuzzing results example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Export Results to CSV")
    print("=" * 60)
    
    fuzzer = RFIDFuzzer(iterations=50)
    
    print("Running fuzzing campaign...")
    stats = fuzzer.fuzz(
        original_key="FFFFFFFFFFFF",
        strategy=MutationStrategy.BYTE,
        iterations=50,
        slowdown=0,
    )
    
    # Export results
    output_file = "fuzzing_results_example.csv"
    fuzzer.export_results(output_file)
    
    print(f"Results exported to {output_file}")
    print(f"Total results: {len(stats.results)}")
    
    # Show first few results
    print("\nFirst 5 results:")
    for result in stats.results[:5]:
        print(f"  Iter {result.iteration}: {result.behavior}")


def main():
    """Run all examples"""
    port = None
    
    # Check if device port specified
    if len(sys.argv) > 1:
        port = sys.argv[1]
        print(f"Using device: {port}\n")
    else:
        print("Using simulator mode (no real device)\n")
    
    try:
        # Run examples
        example_basic_fuzzing()
        example_device_detection(port)
        example_authentication_testing(port)
        example_session_statistics(port)
        example_fuzzing_with_device(port)
        example_error_recovery(port)
        example_export_results()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
