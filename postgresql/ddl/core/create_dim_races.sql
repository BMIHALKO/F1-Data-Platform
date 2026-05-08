create table if not exists core.dim_races (
    season integer not null,
    round_number integer not null,
    race_name text,
    race_date date,
    race_time text,
    circuit_id text,
    profile_url text,

    fp1_date date,
    fp1_time text,
    fp2_date date,
    fp2_time text,
    fp3_date date,
    fp3_time text,

    qualifying_date date,
    qualifying_time text,

    sprint_date date,
    sprint_time text,
    sprint_qualifying_date date,
    sprint_qualifying_time text,

    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    primary key (season, round_number),

    constraint fk_dim_races_circuit
        foreign key (circuit_id)
        references core.dim_circuits (circuit_id)
)