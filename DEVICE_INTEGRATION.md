# Device Integration Guide

## Overview

The ChameleonUltra RFID Fuzzer now features comprehensive device integration for real hardware testing alongside simulator mode. This guide explains the architecture, usage, and configuration options.

## Architecture

### Two-Tier Architecture

```
User Application
        ↓
  Fuzzer CLI
        ↓
   RFIDFuzzer Class
        ↓
 DeviceInterface Layer
        ↓
  Real Hardware / Simulator
```

### Components

1. **DeviceInterface**: Abstraction layer for device communication
   - Handles device detection and validation
   - Manages authentication testing with retry logic
   - Provides session tracking and statistics
   - Supports both real hardware and simulator mode

2. **RFIDFuzzer**: Core fuzzing engine
   - Integrates with DeviceInterface
   - Implements mutation strategies
   - Tracks campaign statistics
   - Supports health checks and recovery

3. **CLI**: Command-line interface
   - Device discovery and configuration
   - Session management
   - Progress reporting
   - Export functionality

## Device Interface

### DeviceInterface Class

```python
from chameleon_fuzzer import DeviceInterface, AuthResult, KeyType

# Create interface (hardware or simulator)
device = DeviceInterface(port="/dev/ttyUSB0")  # Real hardware
device = DeviceInterface()                      # Simulator (default)

# Start session
device.start_session()

# Test authentication
key = bytes.fromhex("FFFFFFFFFFFF")
result, error = device.test_authentication(
    block=0,
    key_type=KeyType.A,
    key=key,
    retry_count=3
)

if result == AuthResult.SUCCESS:
    print("Authentication successful!")
elif result == AuthResult.TIMEOUT:
    # Automatic retry happened
    print("Timeout occurred")

# Get session statistics
stats = device.get_session_stats()
print(f"Success rate: {stats['success_rate']:.1f}%")

# Validate device health
healthy = device.validate_device_health()

# End session and cleanup
device.end_session()
```

### Enums and Data Classes

```python
class DeviceMode(Enum):
    READER = "reader"
    TAG = "tag"
    UNKNOWN = "unknown"

class AuthResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    ERROR = "error"

@dataclass
class DeviceInfo:
    name: str
    hw_version: str
    fw_version: str
    mode: DeviceMode
    supports_reader_mode: bool
    supports_mifare_classic: bool
    device_id: Optional[str] = None
    max_retries: int = 3
    timeout_ms: int = 1000

@dataclass
class FuzzerSession:
    device_info: DeviceInfo
    start_time: float
    mutation_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    error_count: int = 0
    timeout_count: int = 0
```

## Usage Examples

### Basic Fuzzing with Simulator

```bash
# No device specified - uses simulator
chameleon-fuzzer -i 100 -m bit -o results.csv
```

### Real Hardware Fuzzing

```bash
# Connect to device on /dev/ttyUSB0
chameleon-fuzzer -i 500 --device /dev/ttyUSB0 -m byte -o results.csv

# Extended testing with health checks
chameleon-fuzzer -i 1000 \
    --device COM3 \
    --retries 3 \
    --health-check 50 \
    -m xor \
    --verbose
```

### Python API

#### Basic Usage

```python
from chameleon_fuzzer import RFIDFuzzer, DeviceInterface, MutationStrategy, KeyType

# Create fuzzer with device
device = DeviceInterface(port="/dev/ttyUSB0")
fuzzer = RFIDFuzzer(iterations=1000, device_interface=device)

# Run fuzzing campaign
stats = fuzzer.fuzz(
    original_key="FFFFFFFFFFFF",
    strategy=MutationStrategy.BYTE,
    iterations=1000,
    slowdown=0.05,
    target_block=1,
    key_type=KeyType.A,
    retries=3,
    health_check_interval=100,  # Check device every 100 iterations
)

# Print results
fuzzer.print_summary()

# Export results
fuzzer.export_results("fuzzing_results.csv")
```

#### Advanced: Custom Device Interface

```python
from chameleon_fuzzer import RFIDFuzzer, DeviceInterface, AuthResult, KeyType

class CustomDeviceInterface(DeviceInterface):
    """Custom implementation with extended logging"""
    
    def test_authentication(self, block, key_type, key, retry_count=1):
        """Override to add custom logging"""
        print(f"Testing block {block} with key {key.hex()}")
        result, error = super().test_authentication(block, key_type, key, retry_count)
        print(f"Result: {result}")
        return result, error

# Use custom interface
device = CustomDeviceInterface(port="/dev/ttyUSB0")
fuzzer = RFIDFuzzer(device_interface=device)
```

## Configuration

### Device Options

| Option | Default | Description |
|--------|---------|-------------|
| `--device` | None | Serial port for device (e.g., /dev/ttyUSB0, COM3) |
| `--retries` | 1 | Retry attempts on timeout |
| `--health-check` | 0 | Device health check interval (0=disabled) |
| `--verbose` | False | Enable detailed output |

### Device Detection

The fuzzer automatically detects devices on:
- Linux/macOS: `/dev/ttyUSB*`, `/dev/ttyACM*`, `/dev/cu.*`
- Windows: `COM1` through `COM32`

### Connection Parameters

Default timeouts and retry logic:
- **Timeout**: 1000ms per operation
- **Retries**: 3 attempts with exponential backoff
- **Health Check**: Validates device responsiveness

## Error Recovery

### Automatic Recovery Mechanisms

1. **Timeout Handling**
   - Configurable retries with exponential backoff
   - Automatic timeout detection
   - Session continuation after recovery

2. **Connection Recovery**
   - Automatic reconnection on disconnect
   - Device re-initialization
   - Campaign resumption

3. **Health Monitoring**
   - Periodic device responsiveness checks
   - Error threshold detection
   - Graceful degradation

### Recovery Example

```python
device = DeviceInterface(port="/dev/ttyUSB0")

# Automatic retry on timeout
result, error = device.test_authentication(
    block=0,
    key_type=KeyType.A,
    key=bytes.fromhex("FFFFFFFFFFFF"),
    retry_count=3  # Will retry up to 3 times
)

# Validate device health
if not device.validate_device_health():
    print("Device health check failed")
    if device.recover_connection():
        print("Successfully recovered connection")
    else:
        print("Recovery failed")

# Fallback to simulator automatically
# If device unavailable, fuzzer continues with simulator
```

## Session Statistics

### Available Statistics

```python
stats = device.get_session_stats()

# Keys in stats dictionary:
{
    'elapsed_time': float,           # Seconds since session start
    'mutation_count': int,           # Total mutations tested
    'success_count': int,            # Successful authentications
    'failure_count': int,            # Failed authentications
    'error_count': int,              # Errors encountered
    'timeout_count': int,            # Timeouts occurred
    'success_rate': float,           # Percentage (0-100)
    'error_rate': float,             # Percentage (0-100)
    'throughput': float,             # Mutations per second
}
```

### Monitoring During Fuzzing

```python
from chameleon_fuzzer import RFIDFuzzer, DeviceInterface

device = DeviceInterface()
fuzzer = RFIDFuzzer(device_interface=device)

def progress_callback(current, total):
    stats = device.get_session_stats()
    print(f"Progress: {current}/{total}")
    print(f"  Success Rate: {stats['success_rate']:.1f}%")
    print(f"  Throughput: {stats['throughput']:.2f} mut/sec")

fuzzer.fuzz(
    original_key="FFFFFFFFFFFF",
    strategy=MutationStrategy.RANDOM,
    iterations=1000,
    slowdown=0.01,
    health_check_interval=50,
)
```

## Simulator Mode

### When to Use Simulator

1. **Development**: Test fuzzer without hardware
2. **CI/CD**: Automated testing in pipelines
3. **Prototyping**: Quick iteration
4. **Benchmarking**: Performance testing

### Simulator Behavior

- 95% failure rate (typical real device)
- 4% success rate (successful authentications)
- 1% timeout/error rate

### Force Simulator Mode

```python
# Explicitly use simulator (no device)
device = DeviceInterface()  # No port specified = simulator
fuzzer = RFIDFuzzer(device_interface=device)
```

## Testing Device Integration

### Unit Tests

```python
import unittest
from chameleon_fuzzer import RFIDFuzzer, DeviceInterface, MutationStrategy

class TestDeviceIntegration(unittest.TestCase):
    def test_fuzzer_with_device(self):
        """Test fuzzer with real or simulated device"""
        device = DeviceInterface()  # Simulator
        fuzzer = RFIDFuzzer(device_interface=device)
        
        stats = fuzzer.fuzz(
            original_key="FFFFFFFFFFFF",
            strategy=MutationStrategy.BIT,
            iterations=10,
            slowdown=0,
        )
        
        assert len(stats.results) == 10
        assert len(stats.behavior_counts) > 0

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```bash
# Run with simulator (no hardware needed)
pytest tests/test_device_integration.py -v

# Run with real device
pytest tests/test_device_integration.py -v --device COM3

# Run with verbose output
pytest tests/test_device_integration.py -v -s
```

## Troubleshooting

### Device Not Found

```
Error: Device not found on /dev/ttyUSB0
```

**Solutions:**
1. Check device is connected: `ls -la /dev/tty*`
2. Check permissions: `sudo chmod 666 /dev/ttyUSB0`
3. Verify device drivers installed
4. Fall back to simulator: Omit `--device` option

### Timeout Errors

```
Error: Timeout waiting for device response
```

**Solutions:**
1. Increase retries: `--retries 5`
2. Check device responsiveness: `--health-check 10`
3. Reduce load: Increase `--slowdown 0.1`
4. Check device battery/power

### Connection Lost

```
Error: Device disconnected during fuzzing
```

**Solutions:**
1. Check USB cable connection
2. Increase timeout: Device timeout_ms parameter
3. Enable automatic recovery: Device monitors continuously
4. Check system logs for USB errors

## Performance Tuning

### Optimization Tips

1. **Reduce Health Checks**: Lower health_check_interval for speed
2. **Disable Slowdown**: Use `--slowdown 0` for maximum throughput
3. **Batch Operations**: Fuzz multiple blocks in sequence
4. **Session Persistence**: Save results during campaign

### Benchmark Example

```python
import time
from chameleon_fuzzer import RFIDFuzzer, DeviceInterface, MutationStrategy

device = DeviceInterface(port="/dev/ttyUSB0")
fuzzer = RFIDFuzzer(device_interface=device, iterations=1000)

start = time.time()
stats = fuzzer.fuzz(
    original_key="FFFFFFFFFFFF",
    strategy=MutationStrategy.RANDOM,
    iterations=1000,
    slowdown=0,  # No delay
    health_check_interval=0,  # No health checks
)
duration = time.time() - start

throughput = 1000 / duration
print(f"Throughput: {throughput:.2f} mutations/second")
print(f"Total time: {duration:.2f} seconds")
```

## Platform-Specific Notes

### Linux

- Device paths: `/dev/ttyUSB*`, `/dev/ttyACM*`
- Permissions: May need `sudo` or group membership
- Drivers: USB-to-serial drivers usually built-in

### macOS

- Device paths: `/dev/cu.*`, `/dev/tty.*`
- Permissions: May need `sudo` initially
- Drivers: Silicon Labs drivers for some devices

### Windows

- Device paths: `COM1` through `COM32`
- Drivers: USB-to-serial drivers required
- Admin: May need Administrator rights

## Repository Locations

### Main Repository
- **Path**: `software/script/device_interface.py`
- **CLI**: `software/script/chameleon_cli_unit.py` (HFMFFuzzer class)
- **Branch**: `pr/310`

### Standalone Repository
- **Path**: `chameleon_fuzzer/device_interface.py`
- **Fuzzer**: `chameleon_fuzzer/fuzzer.py`
- **CLI**: `chameleon_fuzzer/cli.py`
- **Tests**: `tests/test_device_integration.py`

## Version Compatibility

- Python 3.8+
- ChameleonUltra firmware 0.3.0+
- PySerial 3.5+ (for real hardware)

## Contributing

Device integration improvements welcome:
1. Test on real hardware
2. Report issues with device models
3. Suggest recovery mechanisms
4. Add device profiles

## License

Same as ChameleonUltra project (MIT)
