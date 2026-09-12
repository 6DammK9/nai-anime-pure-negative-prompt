#!/usr/bin/env sh
set -eu

TARGET_COLS="${TARGET_COLS:-40}"

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  echo "Usage: nf40.sh [csv_in] > csv_out"
  echo "If csv_in is omitted, reads from stdin."
  echo "Output is PostgreSQL CSV-compatible with ESCAPE '\\'."
  exit 0
fi

input="${1:-/dev/stdin}"

awk -v target="$TARGET_COLS" '
function emit_row(    i, f, line) {
  if (col == 0 && field == "" && row_started == 0) {
    return
  }

  col++
  cells[col] = field

  if (col < target) {
    for (i = col + 1; i <= target; i++) {
      cells[i] = ""
    }
  } else if (col > target) {
    col = target
  }

  line = ""
  for (i = 1; i <= target; i++) {
    f = cells[i]
    gsub(/\\/, "\\\\", f)
    gsub(/"/, "\\\"", f)
    line = line (i > 1 ? "," : "") "\"" f "\""
  }
  print line

  delete cells
  col = 0
  field = ""
  row_started = 0
}

BEGIN {
  RS = "\0"
  ORS = "\n"
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
        cells[col] = field
        field = ""
        row_started = 1
      } else if (ch == "\n") {
        emit_row()
      } else if (ch == "\r") {
        # ignore CR; LF handles CRLF record breaks
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
    emit_row()
  }
}
' "$input"
