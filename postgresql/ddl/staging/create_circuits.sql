CREATE TABLE IF NOT EXISTS staging.circuits (
    circuit_id TEXT,
    circuit_name TEXT,
    profile_url TEXT,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    locality TEXT,
    country TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);