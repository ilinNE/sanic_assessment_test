-- upgrade --
ALTER TABLE "users" ADD "activation_link" VARCHAR(64) NOT NULL  DEFAULT '';
-- downgrade --
ALTER TABLE "users" DROP COLUMN "activation_link";
