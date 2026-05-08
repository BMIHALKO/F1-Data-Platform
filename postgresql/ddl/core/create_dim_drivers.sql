create table if not exists core.dim_drivers (
    driver_id text primary key,
    permanent_number text,
    driver_code text,
    given_name text,
    family_name text,
    date_of_birth date,
    nationality text,
    profile_url text,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);