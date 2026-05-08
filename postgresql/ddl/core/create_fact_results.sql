create table if not exists core.fact_results (
    season integer not null,
    round_number integer not null,
    driver_id text not null,
    constructor_id text,
    car_number text,

    finishing_position integer,
    position_text text,
    points numeric(8, 2),
    grid_position integer,
    laps_completed integer,
    race_status text,

    finish_time_millis numeric,
    finish_time text,
    
    fastest_lap_rank integer,
    fastest_lap_number integer,
    fastest_lap_time text,

    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    primary key (season, round_number, driver_id),

    constraint fk_fact_results_race
        foreign key (season, round_number)
        references core.dim_races (season, round_number),

    constraint fk_fact_results_driver
        foreign key (driver_id)
        references core.dim_drivers (driver_id),
    
    constraint fk_fact_results_constructor
        foreign key (constructor_id)
        references core.dim_constructors (constructor_id)
)