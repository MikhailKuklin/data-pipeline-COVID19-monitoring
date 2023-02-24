from prefect_dbt.cloud import DbtCloudCredentials

dbt_cloud_credentials = DbtCloudCredentials(api_key="add your API", account_id=148529)

dbt_cloud_credentials.save("covid-dbt-creds", overwrite=True)
