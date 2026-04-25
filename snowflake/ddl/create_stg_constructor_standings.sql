create table if not exists staging.stg_constructor_standings (
    season number,
    standing_position number,
    position_text string,
    points number(6,2),
    wins number,
    constructor_id string,
    ingested_at timestamp_ntz default current_timestamp()
);