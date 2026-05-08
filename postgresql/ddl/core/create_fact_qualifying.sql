create table if not exists core.fact_qualifying (
    season integer not null,
    round_number integer not null,
    driver_id text not null,
    constructor_id text,
    car_number text,
    qualifying_position integer,
    q1_time text,
    q2_time text,
    q3_time text,

    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    primary key (season, round_number, driver_id),
    
    constraint fk_fact_qualifying_race
        foreign key (season, round_number)
        references core.dim_races (season, round_number),

    constraint fk_fact_qualifying_driver
        foreign key (driver_id)
        references core.dim_drivers (driver_id),

    constraint fk_fact_qualifying_constructor
        foreign key (constructor_id)
        references core.dim_constructors (constructor_id)
);