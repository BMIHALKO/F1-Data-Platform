create table if not exists core.fact_driver_standings (
    season integer not null,
    driver_id text not null,
    constructor_id text,
    standing_position integer,
    position_text text,
    point numeric(8, 2),
    wins integer,

    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    primary key (season, driver_id),

    constraint fk_fact_driver_standings_driver
        foreign key (driver_id)
        references core.dim_drivers (driver_id),
    
    constraint fk_fact_driver_standings_constructor
        foreign key (constructor_id)
        references core.dim_constructors (constructor_id)
)