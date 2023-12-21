# Airflow Data Processing Pipeline

## Overview

This project is an Airflow-based data processing pipeline designed to automate the extraction, processing, and storage of data. It utilizes Python operators in Airflow to perform tasks such as downloading data from an API, processing the data based on specific criteria, and saving the processed data to a file system.

## Features

- **Data Downloading:** Automated download of data from a specified API.
- **Data Processing:** Custom logic to filter and process the data.
- **Data Storage:** Saving processed data to a Docker volume for persistence.

![DAG Execution](/images/dag.jpg)

## Prerequisites

- Docker
- Docker Compose
- Apache Airflow 2.7.3 or later

## Installation

1. **Clone the Repository:**
```bash
git clone [https://github.com/nikokarvinen/airflow-docker.git]
cd [airflow-docker]
```

2. **Set Up Docker Compose:**
Update the docker-compose.yml file to match your environment settings, especially the volume configurations.

3.**Build and Run Containers:**
   ```bash
   docker-compose up -d
```

## Usage

Once the setup is complete, you can access the Airflow web interface by navigating to http://localhost:8080 in your web browser. Use the interface to trigger and monitor the pipeline.

### DAG Details

    DAG ID: example_dag
    Schedule: Set to run daily. This can be adjusted in the DAG configuration.
    Tasks:
        download_data: Downloads data from a specified API endpoint.
        process_data: Processes the downloaded data.
        save_data: Saves the processed data to a specified directory.

### Configuration

You can modify the DAG and Python scripts to suit your specific requirements. Make sure to rebuild the Docker images and restart the services after making changes.