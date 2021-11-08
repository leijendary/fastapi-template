-- upgrade --
CREATE UNIQUE INDEX sample_column_1_uidx
    ON sample (column_1)
    WHERE deleted_at IS NULL;

CREATE UNIQUE INDEX sample_translation_name_sample_id_uidx
    ON sample_translation (name, sample_id);