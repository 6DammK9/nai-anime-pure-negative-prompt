DROP TABLE IF EXISTS pgauditlogtofile_extern;

CREATE TEMPORARY TABLE IF NOT EXISTS pgauditlogtofile_extern (
  -- columns 1..17 aligned to normalized pgaudit CSV content
  log_time TIMESTAMPTZ,     -- 1
  user_name text NULL,    -- 2
  database_name text NULL,   -- 3
  process_id text NULL,      -- 4
  connection_from text NULL,    -- 5 (ip:port)
  session_id text NULL,      -- 6
  command_tag text NULL,     -- 7
  session_line_num text NULL,   -- 8
  session_line_subnum text NULL,   -- 9
  sql_state_code text NULL,     -- 10
  audit_type text NULL,      -- 11 (e.g. OBJECT/SESSION)
  statement_id int NULL,    -- 12
  substatement_id int NULL,    -- 13
  "class" text NULL,      -- 14 (e.g. READ/WRITE/DDL)
  command text NULL,      -- 15 (e.g. INSERT/UPDATE)
  object_type text NULL,     -- 16 (e.g. TABLE)
  object_name text NULL,     -- 17 (e.g. public.n8n_chat_histories)

  -- columns 18..40: keep generic payload fragments
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
);

--TRUNCATE pgauditlogtofile_extern;

COPY pgauditlogtofile_extern
--FROM PROGRAM 'tail -n 10 /var/log/postgresql/auditlog/audit-2026-08-10.csv \
--| grep OBJECT \
--| awk ''{ gsub(/\\n/, ""); gsub(/\\"/, ""); }1'' \
--| awk -F'','' ''BEGIN{OFS=","}{
-- if (NF<40) for(i=NF+1;i<=40;i++) $i=""
-- if (NF>40) NF=40
-- print
--}'''
--FROM '/var/log/postgresql/auditlog/audit-2026-08-10.csv'
--FROM '/home/safeuser/pg_dump/audit-objectonly.csv'
FROM PROGRAM '/etc/postgresql/18/main/scripts/nf40.sh /var/log/postgresql/auditlog/audit-2026-08-10.csv'
WITH (FORMAT CSV, HEADER false, ESCAPE '\');

-- SELECT * FROM pgauditlogtofile_extern ORDER BY log_time DESC;

-- Load audit entries (requires parsing the audit message for audit fields)
INSERT INTO audit_log_archive (log_time, user_name, database_name, connection_from, audit_type, statement_id, "class", command, object_type, object_name, statement, raw_log)
SELECT log_time, user_name, database_name, connection_from, audit_type, statement_id, "class", command, object_type, object_name, 
  -- The ugly part breaking CSV, usually JSON object
  concat_ws('', 
    sqlquery_01, sqlquery_02, sqlquery_03, sqlquery_04, sqlquery_05,
    sqlquery_06, sqlquery_07, sqlquery_08, sqlquery_09, sqlquery_10,
    sqlquery_11, sqlquery_12, sqlquery_13, sqlquery_14, sqlquery_15,
    sqlquery_16, sqlquery_17, sqlquery_18, sqlquery_19, sqlquery_20,
    sqlquery_21, sqlquery_22, sqlquery_23
  ) AS statement,
  sqlquery_10 AS raw_log -- Sometimes it shows Client name
FROM pgauditlogtofile_extern;
--WHERE audit_type LIKE 'OBJECT';
--WHERE message LIKE 'AUDIT:%';