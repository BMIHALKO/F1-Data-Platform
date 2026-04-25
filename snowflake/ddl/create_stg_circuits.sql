create table if not exists staging.stg_circuits (
    circuit_id string,
    circuit_name string,
    profile_url string,
    latitude number(9,6),
    longitude number(9,6),
    locality string,
    country string,
    ingested_at timestamp_ntz default current_timestamp()
);