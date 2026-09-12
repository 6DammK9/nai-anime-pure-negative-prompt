CREATE OR REPLACE FUNCTION archive_today_audit_log_nf40(p_run_date date DEFAULT (CURRENT_DATE))
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
-- DROP FUNCTION archive_today_audit_log_nf40(date);
-- SELECT archive_today_audit_log_nf40();
-- SELECT archive_today_audit_log_nf40('2026-08-15');

-- Change '40' for other values if the JSONB over CSV line breaks under this level of awk parsing.
-- Almost entire script is vibed, because all online docs / guides are not solving this question correctly.
-- CSV input: pgauditlogtofile + pgaudit (handles both SESSION and OBJECT), with table name "pgauditlogtofile_extern".
-- Workflow / audit log table: oneuptime, with table name "audit_log_archive".
-- postgres version: 18
DECLARE
    v_file_path text;
    v_cmd       text;
    v_inserted  integer := 0;
    v_file_stat record;
BEGIN

    v_file_path := format(
        '/var/log/postgresql/auditlog/audit-%s.csv',
        to_char(p_run_date, 'YYYY-MM-DD')
    );

    SELECT * INTO v_file_stat FROM pg_stat_file(v_file_path, true);
    IF v_file_stat IS NULL THEN
        RETURN format('Audit file not found: %s', v_file_path);
    END IF;

    -- redirect-audit-csv-to-table.sql
    CREATE TEMP TABLE IF NOT EXISTS pgauditlogtofile_extern (
      -- columns 1..17 aligned to normalized pgaudit CSV content
      log_time TIMESTAMPTZ,
      user_name text NULL,
      database_name text NULL,
      process_id text NULL,
      connection_from text NULL,
      session_id text NULL,
      command_tag text NULL,
      session_line_num text NULL,
      session_line_subnum text NULL,
      sql_state_code text NULL,
      audit_type text NULL,
      statement_id int NULL,
      substatement_id int NULL,
      "class" text NULL,
      command text NULL,

      -- columns 18..40: keep generic payload fragments
      object_type text NULL,
      object_name text NULL,
      sqlquery_01 text NULL,
      sqlquery_02 text NULL,
      sqlquery_03 text NULL,
      sqlquery_04 text NULL,
      sqlquery_05 text NULL,
      sqlquery_06 text NULL,
      sqlquery_07 text NULL,
      sqlquery_08 text NULL,
      sqlquery_09 text NULL,
      sqlquery_10 text NULL,
      sqlquery_11 text NULL,
      sqlquery_12 text NULL,
      sqlquery_13 text NULL,
      sqlquery_14 text NULL,
      sqlquery_15 text NULL,
      sqlquery_16 text NULL,
      sqlquery_17 text NULL,
      sqlquery_18 text NULL,
      sqlquery_19 text NULL,
      sqlquery_20 text NULL,
      sqlquery_21 text NULL,
      sqlquery_22 text NULL,
      sqlquery_23 text NULL
    ) ON COMMIT DROP;

    TRUNCATE pgauditlogtofile_extern;

    -- nf40.sh, $0=v_file_path
    v_cmd := format($cmd$
sh -eu -c 'input=%L
awk -v target=40 -f - "$input" <<'"'"'AWK'"'"'
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
AWK
'
$cmd$, v_file_path);

    EXECUTE format(
        'COPY pgauditlogtofile_extern FROM PROGRAM %L WITH (FORMAT CSV, HEADER false, ESCAPE ''\'')',
        v_cmd
    );

    INSERT INTO audit_log_archive (
      log_time, user_name, database_name, connection_from,
      audit_type, statement_id, "class", command, object_type, object_name,
      statement, raw_log
    )
    SELECT
      log_time,
      user_name,
      database_name,
      connection_from,
      audit_type,
      statement_id,
      "class",
      command,
      object_type,
      object_name,
      concat_ws('',
        sqlquery_01, sqlquery_02, sqlquery_03, sqlquery_04, sqlquery_05,
        sqlquery_06, sqlquery_07, sqlquery_08, sqlquery_09, sqlquery_10,
        sqlquery_11, sqlquery_12, sqlquery_13, sqlquery_14, sqlquery_15,
        sqlquery_16, sqlquery_17, sqlquery_18, sqlquery_19, sqlquery_20,
        sqlquery_21, sqlquery_22, sqlquery_23
      ) AS statement,
      sqlquery_10 AS raw_log
    FROM pgauditlogtofile_extern;

    GET DIAGNOSTICS v_inserted = ROW_COUNT;
    RETURN format('Success: inserted %s rows from %s', v_inserted, v_file_path);

EXCEPTION
    WHEN SQLSTATE '58P01' THEN
        RETURN format('Audit file not found: %s', v_file_path);
END;
$$;
