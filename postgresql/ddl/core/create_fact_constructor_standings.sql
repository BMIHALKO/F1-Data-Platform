create table if not exists core.fact_constructor_standings (
    season integer not null,
    constructor_id text not null,
    standing_position integer,
    position_text text,
    points numeric(10, 6),
    wins integer,

    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    primary key (season, constructor_id),

    constraint fk_fact_constructor_standings_constructor
        foreign key (constructor_id)
        references core.dim_constructors (constructor_id)
)