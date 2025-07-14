CREATE EXTERNAL TABLE IF NOT EXISTS cgm_data (
    timestamp timestamp,
    glucose_mgdl double
)
PARTITIONED BY (
    user_id string,
    date string
)
STORED AS PARQUET
LOCATION 's3://cgm-data-pipeline/'
TBLPROPERTIES (
  'parquet.compress'='SNAPPY'
);