-- upgrade --
CREATE TABLE IF NOT EXISTS "product" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "label" VARCHAR(64) NOT NULL,
    "description" TEXT NOT NULL,
    "price" DECIMAL(12,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "login" VARCHAR(32) NOT NULL UNIQUE,
    "password" VARCHAR(32) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "is_admin" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "bill" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "balance" DECIMAL(15,2) NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "transaction" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "amount" DECIMAL(15,2) NOT NULL,
    "bill_id" INT NOT NULL REFERENCES "bill" ("id") ON DELETE CASCADE,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
