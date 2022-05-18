-- upgrade --
ALTER TABLE "sample" ADD "deleted_by" TEXT;
ALTER TABLE "sample" ADD "created_by" TEXT NOT NULL;
ALTER TABLE "sample" ADD "modified_by" TEXT NOT NULL;
-- downgrade --
ALTER TABLE "sample" DROP COLUMN "deleted_by";
ALTER TABLE "sample" DROP COLUMN "created_by";
ALTER TABLE "sample" DROP COLUMN "modified_by";
