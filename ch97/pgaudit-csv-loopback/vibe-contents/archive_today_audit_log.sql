-- DROP FUNCTION archive_today_audit_log();

CREATE OR REPLACE FUNCTION archive_today_audit_log()
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_file_path text;
    v_inserted  integer := 0;
BEGIN
    -- Build: /var/log/postgresql/auditlog/audit-YYYY-MM-DD.csv
	
    --v_file_path := format(
    --    '/var/log/postgresql/auditlog/audit-%s.csv',
	--	to_char(CURRENT_DATE, 'YYYY-MM-DD')
    --);
	
	v_file_path := '/var/log/postgresql/auditlog/audit-2026-08-10.csv';

    -- Temporary staging table with same structure as target
    CREATE TEMP TABLE tmp_audit_stage
    (LIKE audit_log_archive INCLUDING DEFAULTS INCLUDING GENERATED INCLUDING IDENTITY)
    ON COMMIT DROP;

    -- Load CSV from server filesystem
    --EXECUTE format(
    --    'COPY tmp_audit_stage FROM %L WITH (FORMAT csv, HEADER true)',
    --    v_file_path
    --);

    -- Direct shell
    --EXECUTE format(
    --    'COPY tmp_audit_stage FROM PROGRAM %L WITH (FORMAT csv, HEADER true)',
    --    format(
    --        'cat /var/log/postgresql/auditlog/audit-%s.csv',
    --        to_char(CURRENT_DATE, 'YYYY-MM-DD')
    --    )
    --);

    -- External sh
    COPY tmp_audit_stage FROM PROGRAM '/etc/postgresql/18/main/scripts/nf40.sh /var/log/postgresql/auditlog/audit-2026-08-10.csv' WITH (FORMAT csv, HEADER true);

    -- Insert into archive
    INSERT INTO audit_log_archive
    SELECT * FROM tmp_audit_stage;

    GET DIAGNOSTICS v_inserted = ROW_COUNT;
    -- RETURN v_inserted;
	RETURN format('Success with inserted rows: %', v_inserted);

EXCEPTION
    WHEN SQLSTATE '58P01' THEN  -- undefined_file
        RAISE NOTICE 'Audit file not found: %', v_file_path;
        -- RETURN 0;
		RETURN format('Audit file not found: %s', v_file_path);
END;
$$;