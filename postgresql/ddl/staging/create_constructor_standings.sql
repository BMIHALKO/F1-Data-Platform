CREATE TABLE IF NOT EXISTS staging.constructor_standings (
    season INTEGER,
    standing_position INTEGER,
    position_text TEXT,
    points NUMERIC(6,2),
    wins INTEGER,
    constructor_id TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);