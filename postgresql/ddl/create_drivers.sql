CREATE TABLE IF NOT EXISTS staging.drivers (
    driver_id TEXT,
    permanent_number TEXT,
    driver_code TEXT,
    given_name TEXT,
    family_name TEXT,
    date_of_birth DATE,
    nationality TEXT,
    profile_url TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);