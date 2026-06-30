# 🔐 File Integrity Monitor (FIM)

A security utility designed to detect unauthorized modifications, deletions, or additions to sensitive files using SHA-256 cryptographic hashes.

---

## 🌟 Features

- Generates digital baseline checksums of target directories.
- Alerts on unauthorized file modifications, additions, and deletions.
- JSON-based baseline storage for simple integration.

---

## 🚀 Quick Start

```bash
# 1. Initialize baseline for a target directory
python main.py ./my_folder --init

# 2. Verify file integrity against baseline
python main.py ./my_folder --check
```
