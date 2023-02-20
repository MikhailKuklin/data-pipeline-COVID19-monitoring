
{{ config(materialized='table') }}

with coviddata as (
    select *, 
    from {{ ref('stg_covid') }}
    where (country is not null) and (continent is not null) and (new_cases_per_million is not null) and (new_cases is not null)

) 

select 
    coviddata.date, 
    coviddata.people_vaccinated,
    coviddata.new_cases as total_cases,
    coviddata.continent,
    coviddata.country

 from coviddata
