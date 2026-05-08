insert into core.dim_drivers (
    driver_id,
    permanent_number,
    driver_code,
    given_name,
    family_name,
    date_of_birth,
    nationality,
    profile_url,
    updated_at
)
select distinct on (driver_id)
    driver_id,
    permanent_number,
    driver_code,
    given_name,
    family_name,
    date_of_birth,
    nationality,
    profile_url,
    current_timestamp
from staging.drivers
where driver_id is not null
order by driver_id
on conflict (driver_id)
do update set
    permanent_number = excluded.permanent_number,
    driver_code = excluded.driver_code,
    given_name = excluded.given_name,
    family_name = excluded.family_name,
    date_of_birth = excluded.date_of_birth,
    nationality = excluded.nationality,
    profile_url = excluded.profile_url,
    updated_at = current_timestamp;