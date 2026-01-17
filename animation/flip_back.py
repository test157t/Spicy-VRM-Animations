#!/usr/bin/env python3
import argparse
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?", default=".", help="Directory to scan (recursive).")
    ap.add_argument("--ext", default=".bvh", help="Base extension (default: .bvh)")
    ap.add_argument("--suffix", default="_tmp", help="Suffix to remove (default: _tmp)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.dir).resolve()
    tail = (args.ext + args.suffix).lower()  # ".bvh_tmp"

    renamed = 0
    skipped = 0

    for p in root.rglob("*"):
        if not p.is_file():
            continue

        if not p.name.lower().endswith(tail):
            continue

        dst = Path(str(p)[: -len(args.suffix)])  # foo.bvh_tmp -> foo.bvh
        if dst.exists():
            skipped += 1
            continue

        if args.dry_run:
            print(f"{p} -> {dst}")
        else:
            p.rename(dst)
        renamed += 1

    print(f"Done. Renamed: {renamed}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
