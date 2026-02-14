# ChameleonUltra RFID Fuzzer - User Guide

## Overview
The RFID Fuzzer (`hf mf fuzz`) is a security testing tool that mutates and tests MIFARE Classic tag authentication sequences to identify robustness issues and unexpected behaviors in the device.

## Features
- **Multiple Mutation Types**: bit-level, byte-level, XOR, and random mutations
- **Configurable Testing**: Control iterations, target blocks, and mutation patterns
- **Behavior Logging**: Records all authentication attempts and responses
- **CSV Export**: Save results to file for analysis
- **Reproducibility**: Use seeds for repeatable fuzzing sessions

## Command Syntax
```
hf mf fuzz [options]
```

## Arguments

### Core Options
- `-i, --iterations <dec>`: Number of test iterations (default: 100)
- `-b, --block <dec>`: Target block for fuzzing (default: 0)
- `-t, --target-type {A|B}`: Key type to target (default: A)

### Mutation Control
- `-m, --mutation-type {bit|byte|xor|random}`: Type of mutation to apply (default: bit)
  - **bit**: Flip random bits in the key
  - **byte**: Replace random bytes with random values
  - **xor**: XOR random bytes with random values
  - **random**: Generate completely random keys

### Output & Control
- `-o, --output <file>`: Save results to CSV file
- `--seed <dec>`: Set random seed for reproducible results
- `--slowdown <float>`: Delay between iterations in seconds (default: 0.01)

## Usage Examples

### Basic Fuzzing (100 iterations, default settings)
```
hf mf fuzz
```

### Target Block 3 with Byte Mutations
```
hf mf fuzz -b 3 -m byte -i 200
```

### Fuzzing with Seed (Reproducible)
```
hf mf fuzz --seed 12345 -m bit -i 500
```

### Export Results to CSV
```
hf mf fuzz -o results.csv -i 1000 -m xor
```

### Comprehensive Testing
```
hf mf fuzz -b 5 -t B -m random -i 500 --seed 999 -o fuzz_results.csv --slowdown 0.05
```

## Output Explanation

### Console Output Example
```
 - Starting MIFARE Fuzzer
   Iterations: 100
   Mutation Type: bit
   Target Block: 0
   Target Type: A
   Slowdown: 0.01s
 - Generating test data...
 - Fuzzing in progress...
   Progress: 10/100 (10%)
   ...
 - Fuzzing completed in 15.34 seconds
 - Results Summary:
   Successful Authentications: 2
   Failed Authentications: 95
   Device Errors: 3
   Total Mutations: 100
 - Interesting Behaviors Found: 3
   [15] a0a1a2a3a4a4: ERROR: Device timeout
   [42] a0a1a2a3a4b5: ERROR: Connection lost
   [98] a0a1a2a3a5a5: AUTH_SUCCESS (unexpected!)
```

### CSV Output Format
- **iteration**: Test number
- **mutated_key**: The mutated key that was tested (hex)
- **original_key**: The original base key (hex)
- **behavior**: Result of the test (AUTH_SUCCESS, AUTH_FAIL, ERROR)
- **timestamp**: When the test was performed

## Interpretation

### Success Metrics
- Low number of unexpected AUTH_SUCCESS results suggests strong cryptography
- Consistent timeout patterns may indicate buffer overflow opportunities
- Device errors often signal robustness issues

### Security Implications
- **AUTH_SUCCESS on random keys**: Potential vulnerability!
- **Device crashes/resets**: Potential DoS vulnerability
- **Unusual timing patterns**: May indicate side-channel opportunity

## Tips for Effective Fuzzing

1. **Start Simple**: Use bit mutations with default settings first
2. **Increase Iterations**: Higher iterations = better coverage (500-1000+)
3. **Target Specific Blocks**: Sector trailers (blocks 3, 7, 11...) are most sensitive
4. **Try Different Mutation Types**: Each reveals different behaviors
5. **Use Seeds**: Reproduce interesting findings with the same seed
6. **Analyze CSV Output**: Look for patterns in the results

## Example Analysis Workflow

```
1. Run initial fuzzer: hf mf fuzz -i 200 -o baseline.csv
2. Analyze results for interesting behaviors
3. If interesting behavior found at iteration X:
   - Note the seed or behavior
   - Run again with same/adjusted seed
   - Try different mutation types on same block
   - Check target_type (A vs B)
4. Export detailed findings to documentation
```

## Integration with CLI

The fuzzer is integrated as a subcommand under:
- **Category**: High Frequency (HF) commands
- **Subcategory**: MIFARE Classic (mf)
- **Full Path**: `hf mf fuzz`

To see help in CLI:
```
hf mf fuzz --help
```

## Performance Notes

- Default slowdown (0.01s) prevents overwhelming the device
- Increase slowdown if you experience connection issues
- Decrease for faster testing (may reduce reliability)
- CSV export happens after all tests complete
- Ctrl+C stops testing and saves results

---

**Created for ChameleonUltra RFID Testing Platform**
