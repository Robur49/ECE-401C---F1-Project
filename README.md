# The Pole Position Advantage: F1 Data Analytics 🏎️📈

## 🏁 Project Overview

This project is a database system designed to analyze historical Formula 1 data from 1950 to 2024. Our core task is to determine if starting a race in 1st place ("Pole Position") guarantees a race win, and to quantify how that advantage has changed across different eras of the sport.

By applying strict relational database techniques, we aim to extract precise conversion rates (win percentages) while optimizing query performance for large datasets.

## 🏁 Data Sources

We are utilizing the comprehensive Formula 1 World Championship dataset sourced from Kaggle (originally via the Ergast API). To maintain a strict project scope, our database schema relies on joining just two core tables:

Main Dataset Page: Formula 1 World Championship (1950 - 2024)

Target Tables: races.csv and results.csv (Available via the Data Explorer)

## 🏁 Literature Review & Related Work

Our query approach and statistical outputs are being directly compared against prior data science research conducted on this dataset.

Specifically, we are comparing our methodology with:

Reference: Maroofium's "F1 Performance Insights and Analysis"

Section: Section 13 ("Qualifying vs Race Position")

Note: While the reference material relies heavily on visual scatter plots that suffer from overplotting, our system focuses on utilizing SQL query optimization to return exact mathematical conversion rates.

## 🏁 Database Techniques & Infrastructure

To efficiently process the 26,000+ rows of historical data, this project implements the following database engineering concepts:

Schema Normalization: Organizing entities in 3rd Normal Form (3NF) to separate race event details from individual driver outcomes.

Query Optimization: Using strict INNER JOIN logic on the raceId foreign key to ensure complete data intersection and avoid the implicit conversion pitfalls of LEFT JOIN.

Indexing: Implementing B-Tree indexing on primary and foreign keys (raceId) as well as target search attributes (grid) to reduce I/O costs and eliminate full sequential table scans.

## 🏁 Setup Instructions

(To be updated as infrastructure scripts are finalized)

Download races.csv and results.csv from the Kaggle link above.

Place the CSV files in the root directory.

Run the database initialization script to construct the SQLite schema and ingest the records.
