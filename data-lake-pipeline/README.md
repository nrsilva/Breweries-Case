# Data Lake Pipeline - Brewery Data

This project is a data pipeline that ingests, transforms, and aggregates brewery data from the [Open Brewery DB API](https://api.openbrewerydb.org/). It follows a medallion architecture with three layers: Bronze, Silver, and Gold.

## Project Structure

The project is organized as follows:

data-lake-pipeline/
├── dags/                           # Airflow DAGs (or another orchestration tool)
│   └── brewery_data_pipeline.py    # Main pipeline DAG script
├── src/                            # Source code (data ingestion, transformation, etc)
│   ├── __init__.py
│   ├── ingest_data.py              # Functions for consuming data from the API
│   ├── transform_data.py           # Functions for transforming the data
│   ├── aggregate_data.py           # Functions for aggregating the data (Gold layer)
│   └── utils.py                    # Utility functions (e.g., validation, API connections)
├── data/                           # Raw and transformed data storage
│   ├── raw/                        # Bronze layer: raw data
│   ├── silver/                     # Silver layer: transformed and partitioned data
│   └── gold/                       # Gold layer: aggregated data
├── tests/                          # Automated tests
│   ├── __init__.py
│   ├── test_data_pipeline.py       # Tests for the overall pipeline
│   ├── test_ingest.py              # Tests for data ingestion
│   ├── test_transform.py           # Tests for data transformation
│   └── test_aggregate.py           # Tests for data aggregation
├── docker/                         # Docker related files
│   ├── Dockerfile                  # Dockerfile for containerizing the environment
│   └── docker-compose.yml          # Docker Compose configuration (if necessary)
├── scripts/                        # Helper scripts for manual execution or batch processing
│   ├── run_pipeline.sh             # Shell script to run the pipeline manually
│   └── setup.sh                    # Script to set up the local environment
├── config/                         # Configuration files
│   └── config.yaml                 # Configuration file (API settings, paths, etc)
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
└── setup.py                        # Python setup file



## Project Overview

The `data-lake-pipeline` project uses **Apache Spark** to process brewery data from the Open Brewery DB API. The pipeline is orchestrated using **Airflow** (or another orchestration tool) and processes the data in a medallion architecture, with three layers:

- **Bronze**: Raw data from the API is stored in its original format.
- **Silver**: The data is cleaned, transformed, and partitioned by location in a columnar format (Parquet).
- **Gold**: Aggregated data is created, providing insights such as the number of breweries per type and location.

## Features

- Data ingestion from the Open Brewery DB API.
- Data transformation using Apache Spark and partitioning by location.
- Data aggregation for analytical insights (breweries count by type and location).
- Automated pipeline using Airflow for orchestration.
- Dockerized environment for easy setup and execution.
- Unit tests for key parts of the pipeline (ingestion, transformation, aggregation).

## Requirements

To run this project, you will need:

- Python 3.8 or higher
- Apache Spark (with PySpark)
- Apache Airflow (for orchestration)
- Docker (optional, for containerization)
- Jupyter (optional, for interactive analysis)

### Python Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
