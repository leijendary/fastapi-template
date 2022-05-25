-- upgrade --
DROP INDEX IF EXISTS sample_column_1_uindex;
CREATE UNIQUE INDEX IF NOT EXISTS sample_column_1_uindex
    ON sample (LOWER(column_1))
    WHERE deleted_at IS NULL;
-- downgrade --
DROP INDEX IF EXISTS sample_column_1_uindex;
CREATE UNIQUE INDEX IF NOT EXISTS sample_column_1_uindex
    ON sample (column_1)
    WHERE deleted_at IS NULL;
