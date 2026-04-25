create table if not exists staging.stg_constructors (
    constructor_id string,
    constructor_name string,
    nationality string,
    profile_url string,
    ingested_at timestamp_ntz default current_timestamp()
);