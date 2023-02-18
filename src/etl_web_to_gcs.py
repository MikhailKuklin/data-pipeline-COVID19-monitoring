from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries=2)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean(df=pd.DataFrame) -> pd.DataFrame:
    """Preprocess dataset"""
    df.rename(columns={"location": "country"}, inplace=True)
    print(f"Shape of the dataframe before dropping duplicates: {df.shape}")
    df.drop_duplicates(inplace=True)
    print(f"Shape of the dataframe after dropping duplicates: {df.shape}")
    print(f"columns: {df.dtypes}")
    return df

@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{dataset_file}.parquet")
    df.to_parquet(path)
    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("covid-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return

@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    dataset_file = "covid-data"
    dataset_url = f"https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-{dataset_file}.csv"
    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, dataset_file)
    write_gcs(path)

if __name__ == "__main__":
    etl_web_to_gcs()
