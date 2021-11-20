-- upgrade --
CREATE UNIQUE INDEX sample_column_1_uidx
    ON sample (column_1)
    WHERE deleted_at IS NULL;

CREATE UNIQUE INDEX sample_translation_sample_id_language_uidx
    ON sample_translation (sample_id, language);