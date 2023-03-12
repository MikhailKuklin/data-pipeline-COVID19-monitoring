import os

from prefect import flow
from prefect_dbt.cli.commands import DbtCliProfile, DbtCoreOperation

@flow(log_prints=True)
def dbt_transform():
    dbt_path = "dbt"

    dbt_op = DbtCoreOperation(
        commands=["dbt debug", "dbt run --var 'is_test_run: false'"],
        working_dir=dbt_path,
        project_dir=dbt_path,
        profiles_dir=dbt_path,
    ).run()

if __name__ == "main":
    dbt_transform()
