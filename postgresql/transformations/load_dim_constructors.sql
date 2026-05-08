insert into core.dim_constructors (
    constructor_id,
    constructor_name,
    nationality,
    profile_url,
    updated_at
)
select distinct on (constructor_id)
    constructor_id,
    constructor_name,
    nationality,
    profile_url,
    current_timestamp
from staging.constructors
where constructor_id is not null
order by constructor_id
on conflict (constructor_id)
do update set
    constructor_name = excluded.constructor_name,
    nationality = excluded.nationality,
    profile_url = excluded.profile_url,
    updated_at = current_timestamp;