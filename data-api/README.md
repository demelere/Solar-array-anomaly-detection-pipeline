### Ingestion

Some initial setup for ingesting CSV seed data into the TimeScaleDB table.  

1. First, create the table to match the CSV structure

```CREATE TABLE solar_array_telemetry (
    timestamp TIMESTAMPTZ NOT NULL,
    active_energy_delivered_received DOUBLE PRECISION,
    current_phase_average DOUBLE PRECISION,
    active_power DOUBLE PRECISION,
    performance_ratio DOUBLE PRECISION,
    wind_speed DOUBLE PRECISION,
    weather_temperature_celsius DOUBLE PRECISION,
    weather_relative_humidity DOUBLE PRECISION,
    global_horizontal_radiation DOUBLE PRECISION,
    diffuse_horizontal_radiation DOUBLE PRECISION,
    wind_direction DOUBLE PRECISION,
    weather_daily_rainfall DOUBLE PRECISION,
    radiation_global_tilted DOUBLE PRECISION,
    radiation_diffuse_tilted DOUBLE PRECISION
);

SELECT create_hypertable('solar_array_telemetry', 'timestamp');
```

2. Run `ingest_dummy_csv_to_timescaledb.py` to insert data from the CSV into TimescaleDB.

### AWS deployment
The Docker images are stored on an ECR repository.  Build the TimescaleDB and Docker images, and push them to the ECR repo.  

Then create amn ECS cluster and service to host and run this instance.  