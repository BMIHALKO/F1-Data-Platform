insert into core.dim_circuits (
    circuit_id,
    circuit_name,
    locality,
    country,
    latitude,
    longitude,
    profile_url,
    updated_at
)
select distinct on (circuit_id)
    circuit_id,
    circuit_name,
    locality,
    country,
    latitude,
    longitude,
    profile_url,
    current_timestamp
from staging.circuits
where circuit_id is not null
order by circuit_id
on conflict (circuit_id)
do update set
    circuit_name = excluded.circuit_name,
    locality = excluded.locality,
    country = excluded.country,
    latitude = excluded.latitude,
    longitude = excluded.longitude,
    profile_url = excluded.profile_url,
    updated_at = current_timestamp;