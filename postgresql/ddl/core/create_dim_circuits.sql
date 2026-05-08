create table if not exists core.dim_circuits (
    circuit_id text primary key,
    circuit_name text,
    locality text,
    country text,
    latitude numeric(10, 6),
    longitude numeric(10, 6),
    profile_url text,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);