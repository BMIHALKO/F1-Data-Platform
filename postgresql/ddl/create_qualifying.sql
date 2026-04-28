CREATE TABLE IF NOT EXISTS staging.qualifying (
    season INTEGER,
    round_number INTEGER,
    race_name TEXT,
    race_date DATE,
    car_number TEXT,
    qualifying_position INTEGER,
    driver_id TEXT,
    constructor_id TEXT,
    q1_time TEXT,
    q2_time TEXT,
    q3_time TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);