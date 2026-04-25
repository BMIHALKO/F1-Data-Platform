# F1 Data Platform Architecture Overview

## High-Level Flow

Jolpica API -> Python Ingestion -> Snowflake Staging -> Snowflake Core -> Dashboard

## Main Components
- Python ingestion pipeline
- Snowflake data warehouse
- Transformation layer
- Dashboard layer
- Optional orchestration with Airflow

## Source System

The source system for this project is the Jolpica F1 API, which provides Formula 1 data through Ergast-compatible endpoints.

Initial endpoint groups explored:
- drivers
- constructors
- circuits
- races
- results
- qualifying
- driver standings
- constructor standings

## Initial Staging Layer

The first Snowflake staging layer is expected to include:
- stg_drivers
- stg_constructors
- stg_circuits
- stg_races
- stg_results
- stg_qualifying
- stg_driver_standings
- stg_constructor_standings

The staging layer stores flattened raw API data before transformation into core analytical models.

## Folder Responsibilities
- ingestion/: extraction, transformation, loading
- snowflake/: DDL and views
- dashboard/: visualization layer
- airflow/: orchestration DAGs
- docs/: endpoint inventory, mappings, architecture notes