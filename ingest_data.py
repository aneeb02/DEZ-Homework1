#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
import os
from sqlalchemy import create_engine
from tqdm.auto import tqdm

trip_dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

trip_parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


def ingest_zones(engine, zones_file, zones_table):
    """Ingest taxi zones lookup table."""
    if not os.path.exists(zones_file):
        print(f"Zones file {zones_file} not found, skipping zones table.")
        return
    
    print(f"Ingesting zones from {zones_file}...")
    df_zones = pd.read_csv(zones_file)
    df_zones.to_sql(
        name=zones_table,
        con=engine,
        if_exists='replace',
        index=False
    )
    print(f"Successfully created {zones_table} table with {len(df_zones)} zones.")


def ingest_trips(engine, input_file, target_table, chunksize):
    """Ingest trip data into PostgreSQL database."""
    print(f"Ingesting trips from {input_file}...")
    
    # Read parquet or CSV file
    if input_file.endswith('.parquet'):
        df_iter = pd.read_parquet(input_file)
        # Convert to chunks manually for parquet
        df_iter = [df_iter[i:i+chunksize] for i in range(0, len(df_iter), chunksize)]
    else:
        df_iter = pd.read_csv(
            input_file,
            dtype=trip_dtype,
            parse_dates=trip_parse_dates,
            iterator=True,
            chunksize=chunksize,
        )

    first = True

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )
    
    print(f"Successfully ingested data into {target_table} table.")


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='greentrip', help='PostgreSQL database name')
@click.option('--input-file', required=True, help='Path to CSV or Parquet file for trips data')
@click.option('--target-table', default='greentrips_data', help='Target table name for trips')
@click.option('--zones-file', default='taxi_zone_lookup.csv', help='Path to taxi zones CSV file')
@click.option('--zones-table', default='taxi_zones', help='Target table name for zones')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, input_file, target_table, zones_file, zones_table, chunksize):
    """Ingest NYC taxi zones and trip data into PostgreSQL database."""
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    # Ingest zones table first
    ingest_zones(engine, zones_file, zones_table)
    
    # Ingest trip data
    ingest_trips(engine, input_file, target_table, chunksize)

if __name__ == '__main__':
    run()
    