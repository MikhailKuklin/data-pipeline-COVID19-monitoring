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

1. One has to read with following instructions from [prerequisites_readme first](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/prerequisites_readme.md).
This instruction gives a detailed step-by-step guidelines for required configurations of the tools and services needed for the pipeline.

2. Clone this repo to the VM

3. Go to `infrastructure` folder and run:

```sh
terraform init
terraform plan
terraform apply
```

Terraform will create required resources in GCP.

4. Copy the data from the source to GCP, preprocess it, and copy next to BQ using Prefect

```sh
conda activate covid19
prefect cloud login # or ´prefect orion start` if you don't have or don't want to create an account
prefect deployment build etl_web_to_gcs.py:etl_web_to_gcs -n 'COVID19 data to GCS' --cron "0 9 * * *" -a # creates deployment yaml file and schedule it via CRON on 9 UTC time every day
prefect deployment build etl_gcs_to_bq.py:etl_gcs_to_bq -n 'COVID19 data to BQ' --cron "0 10 * * *" -a # creates deployment yaml file and schedule it via CRON on 10 UTC time every day
tmux # it will allow to run prefect agent in the background when ssh connection will be closed
prefect agent start -q 'default'
```

![Prefect Cloud scheduled pipelines](images/prefect_deployment.png)

5. After that, go to dbt cloud and follow the steps for dbt setup steps from [prerequisites_readme](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/prerequisites_readme.md)). Initialize the project and run:

```sh
dbt build --var 'is_test_run: False'
```

This command will build and execute SQL models and create gold layer table in Big Query.

6. Follow first configuring insturctions for [Lookup Studio](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/visualizations_readme.md)

Final dashboard is located here with `Viewer` mode. To get more detailed information on implementation of the dashboard, get detailed look at the copy of the production dashboard which the `Editor` mode.



