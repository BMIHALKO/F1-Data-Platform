insert into core.fact_constructor_standings (
    season,
    constructor_id,
    standing_position,
    position_text,
    points,
    wins,
    updated_at
)
select distinct on (s.season, s.constructor_id)
    s.season,
    s.constructor_id,
    s.standing_position,
    s.position_text,
    s.points,
    s.wins,
    current_timestamp
from staging.constructor_standings s
where s.season is not null
  and s.constructor_id is not null
  and exists (
      select 1
      from core.dim_constructors c
      where c.constructor_id = s.constructor_id
  )
order by s.season, s.constructor_id
on conflict (season, constructor_id)
do update set
    standing_position = excluded.standing_position,
    position_text = excluded.position_text,
    points = excluded.points,
    wins = excluded.wins,
    updated_at = current_timestamp;