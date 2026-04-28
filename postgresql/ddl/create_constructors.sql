CREATE TABLE IF NOT EXISTS staging.constructors (
    constructor_id TEXT,
    constructor_name TEXT,
    nationality TEXT,
    profile_url TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);