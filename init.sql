-- Initialize the database and create a table for RSS feed articles

CREATE TABLE IF NOT EXISTS news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,  -- Unique title
    publication_timestamp TIMESTAMPTZ,
    weblink TEXT NOT NULL,
    image TEXT,
    tags TEXT,
    summary TEXT
);
