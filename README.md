
# IPL Data Analysis

## Overview

An exploratory data analysis project focused on analyzing Indian Premier League (IPL) match and ball-by-ball data using Python. The project explores team performance, batting and bowling statistics, match venues, dismissal patterns, and over-by-over trends through data cleaning, aggregation, and visualization.

## Tools & Technologies

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn

## Project Workflow

### 1. Data Loading

- Loaded match-level and ball-by-ball IPL datasets using Pandas.
- Examined dataset dimensions and previewed the data.

### 2. Data Cleaning

- Standardized team names across both datasets.
- Replaced missing city values with "Unknown".
- Replaced missing match method values with "Non D/L".

### 3. Exploratory Data Analysis

**Team Performance**
- Calculated and visualized team success rates based on matches won and played.
- Analyzed IPL titles won by teams across seasons.

**Batting Analysis**
- Identified the top 10 run scorers across the dataset.
- Examined the top 10 individual batting performances in a match.
- Calculated and compared batting strike rates.

**Bowling Analysis**
- Identified the top 10 wicket-taking bowlers, excluding run-outs.
- Compared wickets taken and runs conceded in individual match performances.

**Match & Venue Analysis**
- Identified the top 10 cities by number of IPL matches hosted.

**Dismissal & Fielding Analysis**
- Analyzed the frequency of different dismissal types using a logarithmic scale.
- Identified the top 10 fielders by recorded dismissals.

**Over-by-Over Analysis**
- Analyzed total runs scored across overs.
- Examined wicket and extra-run patterns.
- Compared batsman runs across overs.

## Dataset

The project uses two CSV datasets:

- `matches.csv` – Match-level IPL data.
- `deliveries.csv` – Ball-by-ball IPL data.

Both datasets are required to run the analysis.

## How to Run

### 1. Install Dependencies

    pip install numpy pandas matplotlib seaborn

### 2. Run the Python Script

    python IPL.py

Ensure that `matches.csv` and `deliveries.csv` are available in the same directory as the Python script.

## Key Learning Outcomes

- Data cleaning and preprocessing using Pandas.
- Grouping, aggregation, sorting, and merging datasets.
- Calculating cricket performance statistics.
- Working with match-level and ball-by-ball data.
- Creating visualizations using Matplotlib and Seaborn.
- Exploring sports datasets to identify performance trends.

## Author

Sohom Chakraborty

GitHub: [Sohom-2005](https://github.com/Sohom-2005)
