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
    """Clean dataset"""
    df.rename(columns={"location": "country"}, inplace=True)
    print(f"Shape of the dataframe before dropping duplicates: {df.shape}")
    df.drop_duplicates(inplace=True)
    print(f"Shape of the dataframe after dropping duplicates: {df.shape}")
    print(f"columns: {df.dtypes}")
    print(f"The latest date: {df['date'].max()}")
    return df

@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"..data/{dataset_file}.parquet")
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True)
    path = Path(path).as_posix()
    df.to_parquet(path)
    return path

@task()
def test_dataframe_schema(path: Path) -> None:
    """Test for checking schema of the dataset"""
    df = pd.read_parquet(path)
    expected_columns = ['iso_code', 'continent', 'country', 'date', 'total_cases', 'new_cases', 'new_cases_smoothed', 'total_deaths', 'new_deaths', 'new_deaths_smoothed', 'total_cases_per_million', 'new_cases_per_million', 'new_cases_smoothed_per_million', 'total_deaths_per_million', 'new_deaths_per_million', 'new_deaths_smoothed_per_million', 'reproduction_rate', 'icu_patients', 'icu_patients_per_million', 'hosp_patients', 'hosp_patients_per_million', 'weekly_icu_admissions', 'weekly_icu_admissions_per_million', 'weekly_hosp_admissions', 'weekly_hosp_admissions_per_million', 'total_tests', 'new_tests', 'total_tests_per_thousand', 'new_tests_per_thousand', 'new_tests_smoothed', 'new_tests_smoothed_per_thousand', 'positive_rate', 'tests_per_case', 'tests_units', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'total_boosters', 'new_vaccinations', 'new_vaccinations_smoothed', 'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred', 'new_vaccinations_smoothed_per_million', 'new_people_vaccinated_smoothed', 'new_people_vaccinated_smoothed_per_hundred', 'stringency_index', 'population_density', 'median_age', 'aged_65_older', 'aged_70_older', 'gdp_per_capita', 'extreme_poverty', 'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers', 'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand', 'life_expectancy', 'human_development_index', 'population', 'excess_mortality_cumulative_absolute', 'excess_mortality_cumulative', 'excess_mortality', 'excess_mortality_cumulative_per_million']
    assert list(df.columns) == expected_columns

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("covid-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return

@flow()
def web_to_gcs() -> None:
    """The main ETL function"""
    dataset_file = "covid-data"
    dataset_url = f"https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-{dataset_file}.csv"
    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, dataset_file)
    test_dataframe_schema(path)
    write_gcs(path)

if __name__ == "__main__":
    web_to_gcs()
