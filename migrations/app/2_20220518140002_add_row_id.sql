-- upgrade --
ALTER TABLE "sample" ADD "row_id" BIGSERIAL NOT NULL;
CREATE INDEX sample_created_at_row_id_index
	ON "sample" ("created_at" DESC, "row_id" DESC);
-- downgrade --
ALTER TABLE "sample" DROP COLUMN "row_id";
