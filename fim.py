import os
import hashlib
import json
from typing import Dict, Any, List

class FileIntegrityMonitor:
    """
    Monitors system directory files for unauthorized modifications, creation, or deletion using SHA-256 baselines.
    """
    def __init__(self, target_dir: str, baseline_file: str = "baseline.json"):
        self.target_dir = os.path.abspath(target_dir)
        self.baseline_file = baseline_file

    def calculate_file_hash(self, filepath: str) -> str:
        """Calculates SHA-256 checksum for a given file."""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception:
            return ""

    def generate_baseline(self) -> Dict[str, str]:
        """Scans directory and saves baseline hashes to file."""
        baseline = {}
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.target_dir)
                baseline[rel_path] = self.calculate_file_hash(full_path)
        return baseline

    def create_baseline(self) -> int:
        """Saves current file state baseline to JSON."""
        baseline = self.generate_baseline()
        with open(self.baseline_file, 'w') as f:
            json.dump(baseline, f, indent=4)
        return len(baseline)

    def check_integrity(self) -> Dict[str, List[str]]:
        """Compares current directory state against saved baseline."""
        if not os.path.exists(self.baseline_file):
            raise FileNotFoundError(f"Baseline file '{self.baseline_file}' not found. Run --init first.")

        with open(self.baseline_file, 'r') as f:
            baseline = json.load(f)

        current_state = self.generate_baseline()

        modified = []
        added = []
        deleted = []

        # Check modified and deleted
        for rel_path, old_hash in baseline.items():
            if rel_path not in current_state:
                deleted.append(rel_path)
            elif current_state[rel_path] != old_hash:
                modified.append(rel_path)

        # Check added
        for rel_path in current_state:
            if rel_path not in baseline:
                added.append(rel_path)

        return {
            "modified": modified,
            "added": added,
            "deleted": deleted
        }
