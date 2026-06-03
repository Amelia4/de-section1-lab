# Building a Modern Data Pipeline with Python

## Project Overview
This project demonstrates a simple end-to-end Data Engineering pipeline using Python, Pandas, DuckDB, and Pandera. The pipeline follows the Bronze-Silver-Gold architecture to transform raw data into analytics-ready datasets.

## Dataset
- Source: https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv
- Dataset contains restaurant transaction records including total bill, tip amount, customer demographics, and dining time.

## Pipeline Architecture

### Bronze Layer
- Ingest raw CSV data from GitHub.
- Store the original dataset without modification.

### Silver Layer
- Standardize column names.
- Create a new column: `tip_pct`.
- Generate a synthetic `visit_datetime`.
- Store cleaned data in Parquet format.

### Gold Layer
- Aggregate data by sex, smoker status, and day.
- Calculate:
  - Average tip percentage
  - Total revenue
  - Number of transactions

## Data Quality Checks
- Validate that:
  - Total bill >= 0
  - Tip >= 0
  - Tip percentage between 0 and 1
  - Party size >= 1
- Validation performed using Pandera.

## Why Parquet?
- Faster query performance.
- Better compression than CSV.
- Commonly used in modern data lake architectures.

## Key Insight
- Sunday recorded the highest average tip percentage (18.37%).
- Female smokers had the highest average tip percentage among customer groups.

## Technologies Used
- Python
- Pandas
- PyArrow
- DuckDB
- Pandera