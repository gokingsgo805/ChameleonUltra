# ChameleonUltra Standalone RFID Fuzzer

This directory contains the standalone RFID Fuzzer for ChameleonUltra.

## About

The standalone fuzzer has been moved to its own repository for independent distribution and development:

**GitHub**: https://github.com/RfidResearchGroup/ChameleonUltra-Fuzzer

## Installation

```bash
git clone https://github.com/RfidResearchGroup/ChameleonUltra-Fuzzer.git
cd ChameleonUltra-Fuzzer
pip install -e .
```

## Quick Usage

```bash
cham-fuzzer -i 100 -m bit -o results.csv
```

## Documentation

- 📖 [User Guide](../../docs/USER_GUIDE.md)
- 🔧 [Technical Guide](../../docs/TECHNICAL_GUIDE.md)
- 📚 [Full Documentation](https://github.com/RfidResearchGroup/ChameleonUltra-Fuzzer)

## Features

- **4 Mutation Strategies**: bit, byte, xor, random
- **Reproducible Testing**: Seed-based fuzzing
- **CSV Export**: Detailed results
- **CLI Interface**: Full command-line support
- **Python Library**: Import and use programmatically

## Integration

The fuzzer is also integrated into the ChameleonUltra CLI:

```bash
# In ChameleonUltra
hw connect
hf mf fuzz -i 100 -o results.csv
```

## Status

✅ Standalone package available
✅ Integrated into ChameleonUltra CLI (pr/310)
✅ Ready for PyPI distribution
✅ Production-ready v1.0

---

See [ChameleonUltra-Fuzzer repository](https://github.com/RfidResearchGroup/ChameleonUltra-Fuzzer) for the main project.
