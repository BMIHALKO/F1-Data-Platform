insert into core.dim_races (
    season,
    round_number,
    race_name,
    race_date,
    race_time,
    circuit_id,
    profile_url,
    fp1_date,
    fp1_time,
    fp2_date,
    fp2_time,
    fp3_date,
    fp3_time,
    qualifying_date,
    qualifying_time,
    sprint_date,
    sprint_time,
    sprint_qualifying_date,
    sprint_qualifying_time,
    updated_at
)
select distinct on (r.season, r.round_number)
    r.season,
    r.round_number,
    r.race_name,
    r.race_date,
    r.race_time,
    r.circuit_id,
    r.profile_url,
    r.fp1_date,
    r.fp1_time,
    r.fp2_date,
    r.fp2_time,
    r.fp3_date,
    r.fp3_time,
    r.qualifying_date,
    r.qualifying_time,
    r.sprint_date,
    r.sprint_time,
    r.sprint_qualifying_date,
    r.sprint_qualifying_time,
    current_timestamp
from staging.races r
where r.season is not null
  and r.round_number is not null
  and (
      r.circuit_id is null
      or exists (
          select 1
          from core.dim_circuits c
          where c.circuit_id = r.circuit_id
      )
  )
order by r.season, r.round_number
on conflict (season, round_number)
do update set
    race_name = excluded.race_name,
    race_date = excluded.race_date,
    race_time = excluded.race_time,
    circuit_id = excluded.circuit_id,
    profile_url = excluded.profile_url,
    fp1_date = excluded.fp1_date,
    fp1_time = excluded.fp1_time,
    fp2_date = excluded.fp2_date,
    fp2_time = excluded.fp2_time,
    fp3_date = excluded.fp3_date,
    fp3_time = excluded.fp3_time,
    qualifying_date = excluded.qualifying_date,
    qualifying_time = excluded.qualifying_time,
    sprint_date = excluded.sprint_date,
    sprint_time = excluded.sprint_time,
    sprint_qualifying_date = excluded.sprint_qualifying_date,
    sprint_qualifying_time = excluded.sprint_qualifying_time,
    updated_at = current_timestamp;