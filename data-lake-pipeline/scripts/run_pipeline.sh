#!/bin/bash

# This script will execute the entire data pipeline sequentially:
# 1. Data Ingestion
# 2. Data Transformation
# 3. Data Aggregation

echo "Starting the data pipeline..."

# Step 1: Data Ingestion
echo "Ingesting data..."
python src/ingest_data.py

# Check if the ingestion step was successful
if [ $? -ne 0 ]; then
    echo "Data ingestion failed. Exiting pipeline."
    exit 1
fi

# Step 2: Data Transformation
echo "Transforming data..."
python src/transform_data.py

# Check if the transformation step was successful
if [ $? -ne 0 ]; then
    echo "Data transformation failed. Exiting pipeline."
    exit 1
fi

# Step 3: Data Aggregation
echo "Aggregating data..."
python src/aggregate_data.py

# Check if the aggregation step was successful
if [ $? -ne 0 ]; then
    echo "Data aggregation failed. Exiting pipeline."
    exit 1
fi

echo "Pipeline execution completed successfully!"
