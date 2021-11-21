-- upgrade --
CREATE TABLE IF NOT EXISTS "sample" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "column_1" VARCHAR(150) NOT NULL,
    "column_2" VARCHAR(1000),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS "sample_translation" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "language" VARCHAR(2) NOT NULL,
    "ordinal" SMALLINT NOT NULL,
    "name" VARCHAR(150) NOT NULL,
    "description" VARCHAR(1000),
    "reference_id" UUID NOT NULL REFERENCES "sample" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS sample_column_1_uidx
    ON sample (column_1)
    WHERE deleted_at IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS sample_translation_reference_id_language_uidx
    ON sample_translation (reference_id, language);