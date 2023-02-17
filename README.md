# covid19_monitoring

![GitHub Actions](https://github.com/MikhailKuklin/covid19_monitoring/actions/workflows/GHA.yml/badge.svg?&branch=main&kill_cache=1)

WIP Data pipeline for uploading, preprocessing, and visualising COVID19 data 

![Project architecture](images/covid19_monitoring_architecture.png)

This repo includes implementation of a simple pipeline for visualization of COVID19 data.

To run it, one has to read and follow instructions from [prerequisites_readme first](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/prerequisites_readme.md).

Next, install packages from requirements file TODO!

Deploy Prefect stack and setup the schedule TODO!

Prefect jobs will move the data according to the schedule from the source to GCP first, clean and preprocess it, and then copy it to Big Query with creating the dataset with table there.

After that, go to dbt cloud and initialize the project there (follow the steps after finalizing the dbt setup steps from [prerequisites_readme](https://github.com/MikhailKuklin/covid19_monitoring/blob/main/prerequisites_readme.md)).

...


