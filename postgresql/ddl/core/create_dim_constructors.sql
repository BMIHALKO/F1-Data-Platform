create table if not exists core.dim_constructors (
    constructor_id text primary key,
    constructor_name text,
    nationality text,
    profile_url text,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);