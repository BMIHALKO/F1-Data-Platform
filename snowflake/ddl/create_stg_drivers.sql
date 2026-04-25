create table if not exists staging.stg_drivers (
    driver_Id string,
    permanent_number string,
    driver_code string,
    given_name string,
    family_name string,
    date_of_birth date,
    nationality string,
    profile_url string,
    ingested_at timestamp_ntz default current_timestamp()
);