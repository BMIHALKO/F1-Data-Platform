insert into core.fact_driver_standings (
    season,
    driver_id,
    constructor_id,
    standing_position,
    position_text,
    points,
    wins,
    updated_at
)
select distinct on (s.season, s.driver_id)
    s.season,
    s.driver_id,
    s.constructor_id,
    s.standing_position,
    s.position_text,
    s.points,
    s.wins,
    current_timestamp
from staging.driver_standings s
where s.season is not null
  and s.driver_id is not null
  and exists (
      select 1
      from core.dim_drivers d
      where d.driver_id = s.driver_id
  )
  and (
      s.constructor_id is null
      or exists (
          select 1
          from core.dim_constructors c
          where c.constructor_id = s.constructor_id
      )
  )
order by s.season, s.driver_id
on conflict (season, driver_id)
do update set
    constructor_id = excluded.constructor_id,
    standing_position = excluded.standing_position,
    position_text = excluded.position_text,
    points = excluded.points,
    wins = excluded.wins,
    updated_at = current_timestamp;