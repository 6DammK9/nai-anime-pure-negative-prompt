#!/usr/bin/env sh
set -eu

TARGET_COLS="${TARGET_COLS:-40}"

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  echo "Usage: verify-nf40.sh [csv_file ...]"
  echo "If no file is passed, verifies audit-*.csv.nf40 in current folder."
  exit 0
fi

if [ "$#" -gt 0 ]; then
  files="$*"
else
  files=$(ls audit-*.csv.nf40 2>/dev/null || true)
fi

if [ -z "${files:-}" ]; then
  echo "No files to verify." >&2
  exit 1
fi

all_ok=1

for file in $files; do
  if [ ! -f "$file" ]; then
    echo "[missing] $file"
    all_ok=0
    continue
  fi

  awk -v target="$TARGET_COLS" -v name="$file" '
  function check_row(    cols) {
    if (col == 0 && field == "" && row_started == 0) {
      return
    }

    cols = col + 1
    total_rows++

    if (cols != target) {
      bad = 1
      if (first_bad_row == 0) {
        first_bad_row = total_rows
        first_bad_cols = cols
      }
    }

    col = 0
    field = ""
    row_started = 0
  }

  BEGIN {
    RS = "\0"
    bad = 0
    first_bad_row = 0
    first_bad_cols = 0
    total_rows = 0
    in_quote = 0
    col = 0
    field = ""
    row_started = 0
  }

  {
    data = $0
    n = length(data)

    i = 1
    while (i <= n) {
      ch = substr(data, i, 1)

      if (in_quote) {
        if (ch == "\\") {
          nextch = (i < n ? substr(data, i + 1, 1) : "")
          if (nextch == "\"" || nextch == "\\") {
            field = field nextch
            i++
          } else {
            field = field ch
          }
        } else if (ch == "\"") {
          nextch = (i < n ? substr(data, i + 1, 1) : "")
          if (nextch == "\"") {
            field = field "\""
            i++
          } else {
            in_quote = 0
          }
        } else {
          field = field ch
        }
      } else {
        if (ch == "\"") {
          in_quote = 1
          row_started = 1
        } else if (ch == ",") {
          col++
          field = ""
          row_started = 1
        } else if (ch == "\n") {
          check_row()
        } else if (ch == "\r") {
          # ignore CR
        } else {
          field = field ch
          row_started = 1
        }
      }

      i++
    }
  }

  END {
    if (field != "" || col > 0 || row_started) {
      check_row()
    }

    if (bad) {
      printf "%s rows=%d first_bad_row=%d first_bad_cols=%d BAD\n", name, total_rows, first_bad_row, first_bad_cols
      exit 2
    }

    printf "%s rows=%d lengths=[%d] OK\n", name, total_rows, target
  }
  ' "$file" || all_ok=0
done

if [ "$all_ok" -eq 1 ]; then
  exit 0
fi
exit 2
