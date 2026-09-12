#!/usr/bin/env python3
import csv
import glob
import sys
from pathlib import Path

TARGET_COLS = 40


def verify_file(path: Path, target_cols: int = TARGET_COLS) -> tuple[bool, set[int], int]:
    lengths: set[int] = set()
    row_count = 0

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(
            handle,
            delimiter=",",
            quotechar='"',
            escapechar='\\',
            doublequote=True,
        )
        for row in reader:
            lengths.add(len(row))
            row_count += 1

    return lengths == {target_cols}, lengths, row_count


def resolve_inputs(args: list[str]) -> list[Path]:
    if args:
        return [Path(item) for item in args]
    return [Path(p) for p in sorted(glob.glob("audit-*.csv.nf40"))]


def main() -> int:
    paths = resolve_inputs(sys.argv[1:])

    if not paths:
        print("No files to verify. Pass files or keep audit-*.csv.nf40 in current folder.", file=sys.stderr)
        return 1

    all_ok = True
    for path in paths:
        if not path.exists():
            print(f"[missing] {path}")
            all_ok = False
            continue

        ok, lengths, row_count = verify_file(path)
        status = "OK" if ok else "BAD"
        print(f"{path} rows={row_count} lengths={sorted(lengths)} {status}")
        if not ok:
            all_ok = False

    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
