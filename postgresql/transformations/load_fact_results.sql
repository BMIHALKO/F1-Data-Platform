insert into core.fact_results (
    season,
    round_number,
    driver_id,
    constructor_id,
    car_number,
    finishing_position,
    position_text,
    points,
    grid_position,
    laps_completed,
    race_status,
    finish_time_millis,
    finish_time,
    fastest_lap_rank,
    fastest_lap_number,
    fastest_lap_time,
    updated_at
)
select distinct on (r.season, r.round_number, r.driver_id)
    r.season,
    r.round_number,
    r.driver_id,
    r.constructor_id,
    r.car_number,
    r.finishing_position,
    r.position_text,
    r.points,
    r.grid_position,
    r.laps_completed,
    r.race_status,
    r.finish_time_millis,
    r.finish_time,
    r.fastest_lap_rank,
    r.fastest_lap_number,
    r.fastest_lap_time,
    current_timestamp
from staging.results r
where r.season is not null
  and r.round_number is not null
  and r.driver_id is not null
  and exists (
      select 1
      from core.dim_races dr
      where dr.season = r.season
        and dr.round_number = r.round_number
  )
  and exists (
      select 1
      from core.dim_drivers d
      where d.driver_id = r.driver_id
  )
  and (
      r.constructor_id is null
      or exists (
          select 1
          from core.dim_constructors c
          where c.constructor_id = r.constructor_id
      )
  )
order by r.season, r.round_number, r.driver_id
on conflict (season, round_number, driver_id)
do update set
    constructor_id = excluded.constructor_id,
    car_number = excluded.car_number,
    finishing_position = excluded.finishing_position,
    position_text = excluded.position_text,
    points = excluded.points,
    grid_position = excluded.grid_position,
    laps_completed = excluded.laps_completed,
    race_status = excluded.race_status,
    finish_time_millis = excluded.finish_time_millis,
    finish_time = excluded.finish_time,
    fastest_lap_rank = excluded.fastest_lap_rank,
    fastest_lap_number = excluded.fastest_lap_number,
    fastest_lap_time = excluded.fastest_lap_time,
    updated_at = current_timestamp;