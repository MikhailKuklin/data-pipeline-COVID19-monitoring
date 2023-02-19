# copied from https://github.com/discdiver/prefect-zoomcamp/blob/main/blocks/make_gh_block.py

from prefect.filesystems import GitHub

# alternative to creating GitHub block in the UI

gh_block = GitHub(
    name="de-zoom", repository="path to GitHub script"
)

gh_block.save("covid_gh", overwrite=True)
