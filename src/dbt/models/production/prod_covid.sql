
{{ config(
    materialized='incremental',
    partition_by={
      "field": "date",
      "data_type": "timestamp",
      "granularity": "day"
    }
)}}

with coviddata as (
    select *, 
    from {{ ref('stg_covid') }}
    where (country is not null) and (continent is not null) and (new_cases_per_million is not null) and (new_cases is not null)

) 

select 
    EXTRACT(YEAR FROM coviddata.date) as date_year, -- extract the year from the date column
    coviddata.date, 
    coviddata.new_cases as total_cases,
    coviddata.new_cases_per_million as total_cases_per_million,
    coviddata.continent,
    coviddata.country

 from coviddata

{% if is_incremental() %}

  -- this filter will only be applied on an incremental run
  where date > (select max(date) from {{ this }})

{% endif %}