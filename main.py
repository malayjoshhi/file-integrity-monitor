import argparse
import sys
from fim import FileIntegrityMonitor

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

BANNER = f"""{CYAN}
  ___ ___ __  __ 
 | __|_ _|  \/  |
 | _| | || |\/| |
 |_| |___|_|  |_|
{RESET}   Host File Integrity Monitor (FIM) v1.0
"""

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Cryptographic File Integrity Monitor")
    parser.add_argument("dir", help="Target directory to monitor")
    parser.add_argument("--init", action="store_true", help="Generate initial cryptographic baseline")
    parser.add_argument("--check", action="store_true", help="Compare current files against baseline")
    parser.add_argument("-b", "--baseline", default="baseline.json", help="Path to baseline JSON file")

    args = parser.parse_args()

    fim = FileIntegrityMonitor(args.dir, baseline_file=args.baseline)

    if args.init:
        print(f"[*] Generating SHA-256 baseline for: {YELLOW}{args.dir}{RESET}...")
        count = fim.create_baseline()
        print(f"{GREEN}[+] Baseline created successfully! Hashed {count} files -> saved to {args.baseline}{RESET}")
    elif args.check:
        try:
            print(f"[*] Checking integrity of: {YELLOW}{args.dir}{RESET} against {args.baseline}...\n")
            results = fim.check_integrity()
            
            modified = results['modified']
            added = results['added']
            deleted = results['deleted']

            if not (modified or added or deleted):
                print(f"{GREEN}[✓] INTEGRITY OK: No file modifications detected.{RESET}")
            else:
                print(f"{RED}[⚠️] ALERT: Integrity Violations Detected!{RESET}\n")
                if modified:
                    print(f"{YELLOW}[MODIFIED FILES]{RESET}")
                    for f in modified:
                        print(f"  - {f}")
                if added:
                    print(f"\n{GREEN}[NEW FILES ADDED]{RESET}")
                    for f in added:
                        print(f"  + {f}")
                if deleted:
                    print(f"\n{RED}[DELETED FILES]{RESET}")
                    for f in deleted:
                        print(f"  x {f}")
        except FileNotFoundError as e:
            print(f"{RED}[-] Error: {e}{RESET}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
