# covid19_monitoring

![GitHub Actions](https://github.com/MikhailKuklin/covid19_monitoring/actions/workflows/GHA.yml/badge.svg?&branch=main&kill_cache=1)

WIP Data pipeline for uploading, preprocessing, and visualising COVID19 data 

This repo includes implementation of a pipeline for visualization of COVID19 data. Original idea of this pipeline is to have scheduled jobs with regularly updated table. 

![Dashboard](images/dashboard_example.png)

- [Goal](#Goal)
- [Data source](#Data-source)
- [Description of architecture](#Description-of-architecture)

## Goal

Visualizing COVID19 data for a monitoring of the situation and identifying the trends.

## Data source

Data has been provided by [Our World in Data](https://ourworldindata.org/coronavirus).

The source file has been uploaded from [GitHub](https://github.com/owid/covid-19-data).

## Description of architecture

![Project architecture](images/covid19_monitoring_architecture.png)

The source data (raw level) is originally in *csv* format and located in GitHub.

Pipeline is implemented using Google Cloud Platform (GCP).

The source data is partially cleaned, saved as a `parquet` file, and moved sequantially first to GCP bucket (Google Cloud Storage (GCS)) and then to Google Biq Query (silver layer). The whole process is orchestrated by Prefect.

The silver layer data is next transformed by *dbt* for configuring the schema, final cleaning, and saving the resulted data as a table to Big Query. This data (gold layer) is ready for visualizations.

Dashboard has been built from the gold layer data using Lookup Studio (previously Google Data Studio) which is synced with Big Query.

The implementation is limited by GCP usage. At the same time, implementation does not involve any local components which makes it more flexible for collaboration goals e.g. working in a team. 

## Reproducibility

To run it, one has to read and follow instructions from [prerequisites_readme first](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/prerequisites_readme.md).
This instruction gives a detailed step-by-step guidelines for required configurations of the tools and services needed for the pipeline.

Deploy Prefect stack and setup the schedule TODO!

Prefect jobs will move the data according to the schedule from the source to GCP first, clean and preprocess it, and then copy it to Big Query with creating the dataset with table there.

After that, go to dbt cloud and initialize the project there (follow the steps after finalizing the dbt setup steps from [prerequisites_readme](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/prerequisites_readme.md)).

...


