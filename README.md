# covid19_monitoring

![GitHub Actions](https://github.com/MikhailKuklin/covid19_monitoring/actions/workflows/GHA.yml/badge.svg?&branch=main&kill_cache=1)

WIP Data pipeline for uploading, preprocessing, and visualising COVID19 data 

![Project architecture](images/covid19_monitoring_architecture.png)

This repo includes implementation of a pipeline for visualization of COVID19 data. Original idea of this pipeline is to have scheduled jobs with regularly updated table. 

![Dashboard](images/dashboard_example.png)

- [Goal](#Goal)
- [Data source](#Data-source)

## Goal

Visualizing COVID19 data for a monitoring of the situation and identifying the trends.

## Data source

Data has been provided by [Our World in Data](https://ourworldindata.org/coronavirus).

The source file has been uploaded from [GitHub](https://github.com/owid/covid-19-data).

## Reproducibility

To run it, one has to read and follow instructions from [prerequisites_readme first](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/prerequisites_readme.md).
This instruction gives a detailed step-by-step guidelines for required configurations of the tools and services needed for the pipeline.

Deploy Prefect stack and setup the schedule TODO!

Prefect jobs will move the data according to the schedule from the source to GCP first, clean and preprocess it, and then copy it to Big Query with creating the dataset with table there.

After that, go to dbt cloud and initialize the project there (follow the steps after finalizing the dbt setup steps from [prerequisites_readme](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/prerequisites_readme.md)).

...


