-- Create table for audit log storage
CREATE TABLE audit_log_archive (
    id BIGSERIAL PRIMARY KEY,
    log_time TIMESTAMPTZ,
    user_name TEXT,
    database_name TEXT,
    connection_from TEXT,
    audit_type TEXT,
    statement_id INT,
    class TEXT,
    command TEXT,
    object_type TEXT,
    object_name TEXT,
    statement TEXT,
    raw_log TEXT
);

-- Create indexes for common queries
CREATE INDEX idx_audit_log_time ON audit_log_archive(log_time);
CREATE INDEX idx_audit_user ON audit_log_archive(user_name);
CREATE INDEX idx_audit_object ON audit_log_archive(object_name);