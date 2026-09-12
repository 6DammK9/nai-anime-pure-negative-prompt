#!/usr/bin/env bash
set -euo pipefail

TARGET_COLS=40

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  shopt -s nullglob
  files=(audit-*.csv)
fi

if [ "${#files[@]}" -eq 0 ]; then
  echo "No input CSV found. Pass files or keep audit-*.csv in current folder." >&2
  exit 1
fi

python - "$TARGET_COLS" "${files[@]}" <<'PY'
import csv
import sys
from pathlib import Path

target_cols = int(sys.argv[1])
files = sys.argv[2:]

for raw_path in files:
    path = Path(raw_path)
    if not path.exists():
        print(f"[skip] not found: {path}", file=sys.stderr)
        continue

    out_path = path.with_suffix(path.suffix + ".nf40")

    with path.open("r", encoding="utf-8", newline="") as src, out_path.open(
        "w", encoding="utf-8", newline=""
    ) as dst:
        reader = csv.reader(src)
        writer = csv.writer(dst, quoting=csv.QUOTE_ALL, lineterminator="\n")

        row_count = 0
        for row in reader:
            if len(row) < target_cols:
                row.extend([""] * (target_cols - len(row)))
            elif len(row) > target_cols:
                row = row[:target_cols]
            writer.writerow(row)
            row_count += 1

    print(f"[ok] {path} -> {out_path} ({row_count} rows)")
PY
