# ChameleonUltra Standalone RFID Fuzzer - Release v1

This is the release branch for ChameleonUltra Standalone RFID Fuzzer v1.0.

## Branch Information

- **Branch**: `release/standalone-fuzzer-v1`
- **Base**: ChameleonUltra main
- **Purpose**: Distribution-ready standalone fuzzer
- **Status**: Release Ready

## What's Included

✅ Complete RFID fuzzer with 4 mutation strategies
✅ Full CLI interface
✅ Comprehensive documentation (850+ lines)
✅ Unit tests (20+ tests)
✅ Example scripts
✅ Setup.py for PyPI distribution
✅ MIT License

## Key Features

### Mutation Strategies
- **Bit-level**: Single bit XOR mutations
- **Byte-level**: Random byte replacement
- **XOR-based**: Pattern XOR operations
- **Random**: Completely random keys

### Reproducibility
- Seed-based fuzzing for exact replay
- Consistent results across runs
- Regression testing support

### Results Export
- CSV format with full details
- Timestamps and behavior tracking
- Statistical analysis support

## Installation

```bash
pip install cham-fuzzer
```

Or from source:

```bash
git clone --branch release/standalone-fuzzer-v1 https://github.com/RfidResearchGroup/ChameleonUltra.git
cd ChameleonUltra
pip install -e .
```

## Quick Start

```bash
cham-fuzzer -i 100 -m bit -o results.csv
```

## Documentation

- README.md - Overview and quick start
- docs/USER_GUIDE.md - Detailed user guide
- docs/TECHNICAL_GUIDE.md - Architecture and implementation
- CONTRIBUTING.md - Contribution guidelines
- CHANGELOG.md - Release notes

## Integration Versions

This standalone fuzzer exists in multiple forms:

1. **Integrated CLI Command** (pr/310)
   - Built into ChameleonUltra CLI
   - Command: `hf mf fuzz`
   - Part of main project

2. **Standalone Package** (feature/standalone-fuzzer)
   - Independent distribution
   - PyPI package: `cham-fuzzer`
   - Separate repository: https://github.com/RfidResearchGroup/ChameleonUltra-Fuzzer

3. **Release Branch** (release/standalone-fuzzer-v1)
   - Optimized for distribution
   - Version-tagged releases
   - This branch

## Branches Overview

```
main ─────────────────────────────────────
 ├─ pr/310 (Integrated Fuzzer)
 ├─ feature/standalone-fuzzer (Standalone Ref)
 └─ release/standalone-fuzzer-v1 (Distribution)
     └─ ChameleonUltra-Fuzzer (independent repo)
```

## Files & Structure

```
└── fuzzer-standalone/
    └── README.md (reference to standalone project)

// Full implementation in independent repo:
ChameleonUltra-Fuzzer/
├── chameleon_fuzzer/      # Main package
│   ├── __init__.py
│   ├── fuzzer.py          # Core engine
│   ├── mutations.py       # Mutation strategies
│   └── cli.py             # CLI interface
├── docs/                  # Documentation
├── examples/              # Example scripts
├── tests/                 # Unit tests
├── setup.py               # PyPI config
└── requirements.txt       # Dependencies
```

## Testing

```bash
pytest tests/
pytest --cov=chameleon_fuzzer tests/
```

## Release Information

- **Version**: 1.0.0
- **Release Date**: February 13, 2026
- **License**: MIT
- **Status**: Production Ready

## Contributing

Contributions welcome! See CONTRIBUTING.md

## Support

- 📖 [Documentation](https://github.com/RfidResearchGroup/ChameleonUltra-Fuzzer)
- 🐛 [Issues](https://github.com/RfidResearchGroup/ChameleonUltra-Fuzzer/issues)
- 💬 [Discussions](https://github.com/RfidResearchGroup/ChameleonUltra)

## Related Projects

- [ChameleonUltra](https://github.com/RfidResearchGroup/ChameleonUltra) - Main project
- [ChameleonUltra-Fuzzer](https://github.com/RfidResearchGroup/ChameleonUltra-Fuzzer) - Standalone distribution
- [RFID Research Group](https://github.com/RfidResearchGroup) - Organization

---

**This is a release branch optimized for standalone distribution.**

To use the integrated version, switch to `pr/310` branch.
To use as independent package, clone from ChameleonUltra-Fuzzer repository.
