# execure from src folder

from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs() -> Path:
    """Download data from GCS"""
    gcs_path = f"data/covid-data.parquet"
    #gcs_block = GcsBucket.load("prefect-gcs")
    gcs_block = GcsBucket.load("covid-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data")
    return Path(f"../data/{gcs_path}")

@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning"""
    df = pd.read_parquet(path)
    df = df[df['continent'].notna()] # remove NaNs continents
    return df

@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    #gcp_credentials_block = GcpCredentials.load("prefect-gcp-creds")
    gcp_credentials_block = GcpCredentials.load("covid-gcp-creds")

    df.to_gbq(
        destination_table=f"covid19.covid_data",
        location = 'europe-west6',
        project_id="prime-framing-374716",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="replace",
    )

@flow()
def gcs_to_bq(log_prints=True):
    """Main ETL flow to load data into Big Query"""

    path = extract_from_gcs()
    df = transform(path)
    write_bq(df)

if __name__ == "__main__":
    gcs_to_bq()
