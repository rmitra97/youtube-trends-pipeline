README - YouTube Trending ETL Pipeline 

This repository contains the data ingestion pipeline for a research project on YouTube Trending dynamics and uplift modeling. The goal is to automatically collect daily data from the YouTube Data API and Google Trends, store timestamped datasets, and prepare a clean foundation for downstream causal inference and modeling.

The pipeline is designed to run in a lightweight, fully automated manner using GitHub Actions, with plans to migrate to Google Cloud Composer (Airflow) or BigQuery/GCS for production-scale orchestration.
The repository follows a modular architecture


Core Components:
- ETL Script (etl/youtube_trends_daily.py)

- Fetches YouTube Trending metadata (snippet, statistics, contentDetails)

- Collects Google Trends search signals

- Appends run_timestamp to every dataset

- Saves outputs in data/ as daily-partitioned CSV files

- Structure mirrors tasks in an Airflow DAG


Purpose

This pipeline forms the data foundation for analyzing whether appearing on YouTube’s Trending page generates measurable uplift in views, engagement, or subscriber growth — and supporting predictive models to estimate trending likelihood.
