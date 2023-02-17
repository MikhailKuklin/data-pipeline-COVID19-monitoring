
{{ config(materialized='table') }}

with coviddata as (
    select *, 
    from {{ ref('stg_covid') }}
    where (total_cases is not null) and (country is not null)

) 


select 
    coviddata.total_cases,
    coviddata.country

 from coviddata
