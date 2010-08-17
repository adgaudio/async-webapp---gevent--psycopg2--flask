BEGIN;

    DROP TABLE IF EXISTS "users" CASCADE;
    CREATE TABLE users(
        "id" SERIAL PRIMARY KEY,
        "email" VARCHAR(64) NOT NULL UNIQUE,
        "name" VARCHAR(64) NOT NULL
    );

    DROP TABLE IF EXISTS "posts" CASCADE;
    CREATE TABLE posts(
        "id" SERIAL PRIMARY KEY,
        "author" INT REFERENCES users(id) ON DELETE RESTRICT,
        "public" BOOLEAN DEFAULT true,
        "title" VARCHAR(128) NOT NULL,
        "text" TEXT NOT NULL,
        "created" TIMESTAMP DEFAULT now(),
        "updated" TIMESTAMP DEFAULT now()
    );

    DROP TABLE IF EXISTS "tags" CASCADE;
    CREATE TABLE tags(
        "path" VARCHAR(64) PRIMARY KEY,
        "name" VARCHAR(64) NOT NULL
    );

    DROP TABLE IF EXISTS "tags_posts" CASCADE;
    CREATE TABLE tags_posts(
        "id" SERIAL PRIMARY KEY,
        "posts_id" INT REFERENCES posts(id) ON DELETE CASCADE,
        "tags_path" VARCHAR(64) REFERENCES tags(path) ON DELETE CASCADE
    );

    DROP TABLE IF EXISTS "comments" CASCADE;
    CREATE TABLE comments(
        "id" SERIAL PRIMARY KEY,
        "author_name" VARCHAR(32) NOT NULL,
        "author_email" VARCHAR(64) NULL,
        "created" TIMESTAMP DEFAULT now(),
        "text" TEXT NOT NULL
    );

COMMIT;
