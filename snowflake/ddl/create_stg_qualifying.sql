create table if not exists staging.stg_qualifying (
    season number,
    round_number number,
    race_name string,
    race_date date,
    car_number string,
    qualifying_position number,
    driver_id string,
    constructor_id string,
    q1_time string,
    q2_time string,
    q3_time string,
    ingested_at timestamp_ntz default current_timestamp()
);