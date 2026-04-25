# Jolpica API Endpoint Inventory

## Core Endpoints
- drivers
- constructors
- circuits
- races
- results
- qualifying
- standings

## Endpoint Notes

### drivers
- Endpoint: `/drivers.json`
- Full URL: `https://api.jolpi.ca/ergast/f1/drivers.json`
- Purpose: Driver reference/master data
- Expected Snowflake target: `stg_drivers`
- Pagination:
    - `limit` defaults to 30
    - max `limit` is 100
    - `offset` controls pagination

#### Response Structure
- MRData
- DriverTable
- Drivers

#### Driver Fields Observed / Expected
- driverId
- url
- givenName
- familyName
- dateOfBirth
- nationality

#### Driver Fields Sometime Present
- permanentNumber
- code

#### Notes
This endpoint should become a driver reference staging table.

The `permanentNumber` and `code` fields may be missing for older historical drivers, so the Snowflake staging table should allow these fields to be nullable


### constructors
- Endpoint: `/constructors.json`
- Full URL: `https://api.jolpi.ca/ergast/f1/constructors.json`
- Purpose: Constructor/team reference data
- Expected Snowflake target: `stg_constructors`
- Pagination:
    - `limit` defaults to 30
    - max `limit` is 100
    - `offset` controls pagination

#### Response Structure
- MRData
- ConstructorTable
- Constructors

#### Constructor Fields Observed / Expected
- constructorId
- url
- name
- nationality

#### Constructor Fields Sometimes Present
- None observed yet

#### Notes
This endpoint should become a constructor reference staging table

### circuits
- Endpoint: `/circuits.json`
- Full URL: `http://api.jolpi.ca/ergast/f1/circuits.json`
- Purpose: Circuit/location reference data
- Expected Snowflake target: `stg_circuits`
- Pagination:
    - `limit` defaults to 30
    - max `limit` is 100
    - `offset` controls pagination

#### Response Structure
- MRData
- CircuitTable
- Circuits
- Location

#### Circuit Fields Observed / Expected
- ciruitId
- url
- circuitName
- Location

#### Circuit Nested Fields Observed / Expected
- Location.lat
- Location.long
- Location.locality
- Location.country

#### Circuit Fields Sometimes Present
- None observed yet

#### Notes
This endpoint should becomes circuit reference staging table

The `Location` object is nested, so these should be flattened into Snowflake columns such as `latitude`, `longitude`, `locality`, and `country`

### races
- Endpoint: `/current/races.json`
- Full URL: `https://api.jolpi.ca/ergast/f1/current/races.json`
- Purpose: Race calendar and event metadata
- Expected Snowflake target: `stg_races`
- Pagination:
    - `limit` defaults 30
    - max `limit` is 100
    - `offset` controls pagination

#### Response Structre
- MRData
- RaceTable
- Races
- Circuit
- Session objects

#### Race Fields Observed / Expected
- season
- round
- url
- raceName
- Circuit
- date
- time
- FirstPractice
- SecondPractice
- ThirdPractice
- Qualifying

#### Race Fields Sometimes Present
- Sprint
- Sprint Qualifying

#### Notes
This endpoint should become a race calendar staging table.

The `Circuit` obejct is nested, but for staging we should likely keep only `Circuits.circuitId` as `circuitId`.

Spring-related fields only appear on sprint weekends, so `Sprint` and `SprintQuialifying` should be nullable.

`SecondPractice` and `ThirdPractice` may be missing on sprint weekends, so those fields should also be nullable.


### results
- Endpoint: `/current/last/results.json`
- Full URL: `https://api.jolpi.ca/ergast/f1/current/last/results.json`
- Purpose: Race result fact data
- Expected Snowflake target: `stg_results`
- Pagination:
    - `limit` deafults to 30
    - max `limit` is 100
    - `offset` controls pagination

#### Response Structure
- MRData
- RaceTable
- Races
- Results
- Driver
- Constructor
- Time
- FastestLap

#### Result Fields Observed / Expected
- number
- position
- positionText
- points
- Driver
- Constructor
- grid
- laps
- status
- Time
- FastestLap

#### Results Nested Fields Observed / Expected
- Driver.driverId
- Driver.permanentNumber
- Driver.code
- Driver.givenName
- Driver.familyName
- Driver.dateOfBirth
- Driver.nationality
- Constructor.constructorId
- Constructor.name
- Constructor.nationality
- Time.millis
- Time.time
- FastestLap.rank
- FastestLap.lap
- FastestLap.Time

#### Results
- Time
- Time.millis
- Time.time
- FastestLap.Time.time

#### Notes
This endpoint should become a race results staging table.

The `Driver` and `Constructor` objects are nested, but for staging results we should primarily keep `Driver.driverId` and `Constructor.constructorId`.

The `Time` object may be missing for retired drivers, so race time fields should be nullable.

`positionText` can contain non-numeric values such as `R`, so it should remain a text field.

### qualifying
- Endpoint: `/current/last/qualifying.json`
- Full URL: `https://api.jolpi.ca/ergast/f1/current/last/qualifying.json`
- Purpose: Qualifying session performance
- Expected Snowflake target: `stg_qualifying`
- Pagination:
    - `limit` defaults to 30
    - max `limit` is 100
    - `offset` controls pagination

#### Response Structure
- MRData
- RaceTable
- Races
- QualifyingResults
- Driver
- Constructor

#### Qualifying Fields Observed / Expected
- number
- position
- Driver
- Constructor
- Q1
- Q2
- Q3

#### Qualifying Nested Fields Observed / Expected
- Driver.driverId
- Driver.permanentNumber
- Driver.code
- Driver.url
- Driver.givenName
- Driver.familyName
- Driver.dateOfBirth
- Driver.nationality
- Constructor.constructorId
- Constructor.url
- Constructor.name
- Constructor.nationality

#### Qualifying Fields Sometime Present
- Q2
- Q3

#### Notes
This endpoint should become a qulaifying results staging table.

The `Driver` and `Constructor` objects are nested, but for staging qualifying results we should primarily keep `Driver.driverId` and `Constructor.constructorId`.

`Q2` may be missing for drivers eliminated in Q1.

`Q3` may be missing for drivers eliminated in Q2.

### driver standings
- Endpoint: `/current/driverStandings.json`
- Full URL: `https://api.jolpi.ca/ergast/f1/current/driverStandings.json`
- Purpose: Championship standings
- Expected Snowflake target: `stg_driver_standings`
- Pagination:
    - `limit` defaults to 30
    - max `limit` is 100
    - `offset` controls pagination

#### Response Structure
- MRData
- StandingsTable
- StandingsLists
- DriverStandings
- Driver
- Constructors

#### Standing Fields Observed / Expected
- position
- positionText
- points
- wins
- Driver
- Constructors

#### Standing Nested Fields Observed / Expected
- Driver.driverId
- Driver.permanentNumber
- Driver.code
- Driver.url
- Driver.givenName
- Driver.familyName
- Driver.dateOfBirth
- Driver.nationality
- Constructors.constructorId
- Constructors.url
- Constructors.name
- Constructors.nationality

#### Standing Fields Sometimes Present
- None observed yet

#### Notes
This endpoint should become a driver standings staging table.

The `Driver` object is nested, but for staging driver standings we should primarily keep `Driver.driverid`.

The `Constructors` field is an array, so for staging we should likely flatten the first construct as `constructor_id`, while keeping in mind that a driver could theoretically be associated with more than one constructor across a season.

### constructor standings
- Endpoint: `/current/constructorStandings.json`
- Full URL: `https://api.jolpi.ca/ergast/f1/current/constructorStandings.json`
- Purpose: Current season constructor championship standings
- Expected Snowflake target: `stg_constructor_standings`
- Pagination:
    - `limit` defaults to 30
    - max `limit` is 100
    - `offset` controls pagination

#### Response Structure
- MRData
- StandingsTable
- StandingsLists
- ConstructorStandings
- Constructor

#### Constructor Standing Fields Observed / Expected
- position
- positionText
- points
- wins
- Constructor

#### Constructor Standing Nested Fields Observed / Expected
- Constructor.constructorId
- Constructor.url
- Constructor.name
- Constructor.nationality

#### Constructor Standing Fields Sometimes Present
- None observed yet

#### Notes
This endpoint should become a constructor standings staging table.

The `Constructor` object is nested, but for staging constructor standings we should primarily keep `Constructor.constructorId`.

## JSON Structure
To be filled after endpoint inspection:
- top-level object structure
- nested arrays
- nullable fields
- pagination behavior

## Snowflake Table Mapping
To be filled after source field analysis:
- source field → staging column
- nested object flattening strategy
- datatype notes