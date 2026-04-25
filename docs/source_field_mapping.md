# Source Field Mapping

## Drivers Endpoint

| Source Field | Target Table | Target Column | Notes |
|---|---|---|---|
| driverId | stg_drivers | driver_id | Primary driver identifier |
| permanentNumber | stg_drivers | permanent_number | Nullable for historical drivers |
| code | stg_drivers | driver_code | Nullable for historical drivers |
| givenName | stg_drivers | given_name | Driver first name |
| familyName | stg_drivers | family_name | Driver last name |
| dateOfBirth | stg_drivers | date_of_birth | ISO date |
| nationality | stg_drivers | nationality | Driver nationality |
| url | stg_drivers | profile_url | Reference URL |

## Constructors Endpoint

| Source Field | Target Table | Target Column | Notes |
|---|---|---|---|
| constructorId | stg_constructors | constructor_id | Primary constructor identifier |
| name | stg_constructors | constructor_name | Team name |
| nationality | stg_constructors | nationality | Constructor nationality |
| url | stg_constructors | profile_url | Reference URL |

## Circuits Endpoint

| Source Field | Target Table | Target Column | Notes |
|---|---|---|---|
| circuitId | stg_circuits | circuit_id | Primary circuit identifier |
| circuitName | stg_circuits | circuit_name | Circuit display name |
| url | stg_circuits | profile_url | Reference URL |
| Location.lat | stg_circuits | latitude | Stored as decimal |
| Location.long | stg_circuits | longitude | Stored as decimal |
| Location.locality | stg_circuits | locality | City/local area |
| Location.country | stg_circuits | country | Country |

## Races Endpoint

| Source Field | Target Table | Target Column | Notes |
|---|---|---|---|
| season | stg_races | season | Season year |
| round | stg_races | round_number | Race round number |
| raceName | stg_races | race_name | Official race name |
| date | stg_races | race_date | Race date |
| time | stg_races | race_time | Nullable if absent |
| Circuit.circuitId | stg_races | circuit_id | Foreign-key candidate to circuits |

## Results Endpoint

| Source Field | Target Table | Target Column | Notes |
|---|---|---|---|
| number | stg_results | car_number | Nullable historically |
| position | stg_results | finishing_position | Nullable if retired/DNF |
| positionText | stg_results | position_text | Includes DNF/DNS text |
| points | stg_results | points | Points awarded |
| grid | stg_results | grid_position | Starting position |
| laps | stg_results | laps_completed | Completed laps |
| status | stg_results | race_status | Finish status |
| Driver.driverId | stg_results | driver_id | Foreign-key candidate to drivers |
| Constructor.constructorId | stg_results | constructor_id | Foreign-key candidate to constructors |
| Time.time | stg_results | finish_time | Nullable |
| FastestLap.rank | stg_results | fastest_lap_rank | Nullable |
| FastestLap.Time.time | stg_results | fastest_lap_time | Nullable |
| FastestLap.AverageSpeed.speed | stg_results | fastest_lap_speed | Nullable |

## Qualifying Endpoint

| Source Field | Target Table | Target Column | Notes |
|---|---|---|---|
| number | stg_qualifying | car_number | Driver car number |
| position | stg_qualifying | qualifying_position | Final qualifying position |
| Driver.driverId | stg_qualifying | driver_id | Foreign-key candidate to drivers |
| Constructor.constructorId | stg_qualifying | constructor_id | Foreign-key candidate to constructors |
| Q1 | stg_qualifying | q1_time | Nullable |
| Q2 | stg_qualifying | q2_time | Nullable; missing if eliminated in Q1 |
| Q3 | stg_qualifying | q3_time | Nullable; missing if eliminated in Q2 |

## Driver Standings Endpoint

| Source Field | Target Table | Target Column | Notes |
|---|---|---|---|
| position | stg_driver_standings | standing_position | Current championship position |
| positionText | stg_driver_standings | position_text | Text version of position |
| points | stg_driver_standings | points | Championship points |
| wins | stg_driver_standings | wins | Number of wins |
| Driver.driverId | stg_driver_standings | driver_id | Foreign-key candidate to drivers |
| Constructors[0].constructorId | stg_driver_standings | constructor_id | First constructor in constructors array |

## Constructor Standings Endpoint

| Source Field | Target Table | Target Column | Notes |
|---|---|---|---|
| position | stg_constructor_standings | standing_position | Current constructor championship position |
| positionText | stg_constructor_standings | position_text | Text version of position |
| points | stg_constructor_standings | points | Constructor championship points |
| wins | stg_constructor_standings | wins | Number of wins |
| Constructor.constructorId | stg_constructor_standings | constructor_id | Foreign-key candidate to constructors |