insert into core.fact_qualifying (
    season,
    round_number,
    driver_id,
    constructor_id,
    car_number,
    qualifying_position,
    q1_time,
    q2_time,
    q3_time,
    updated_at
)
select distinct on (q.season, q.round_number, q.driver_id)
    q.season,
    q.round_number,
    q.driver_id,
    q.constructor_id,
    q.car_number,
    q.qualifying_position,
    q.q1_time,
    q.q2_time,
    q.q3_time,
    current_timestamp
from staging.qualifying q
where q.season is not null
  and q.round_number is not null
  and q.driver_id is not null
  and exists (
      select 1
      from core.dim_races r
      where r.season = q.season
        and r.round_number = q.round_number
  )
  and exists (
      select 1
      from core.dim_drivers d
      where d.driver_id = q.driver_id
  )
  and (
      q.constructor_id is null
      or exists (
          select 1
          from core.dim_constructors c
          where c.constructor_id = q.constructor_id
      )
  )
order by q.season, q.round_number, q.driver_id
on conflict (season, round_number, driver_id)
do update set
    constructor_id = excluded.constructor_id,
    car_number = excluded.car_number,
    qualifying_position = excluded.qualifying_position,
    q1_time = excluded.q1_time,
    q2_time = excluded.q2_time,
    q3_time = excluded.q3_time,
    updated_at = current_timestamp;