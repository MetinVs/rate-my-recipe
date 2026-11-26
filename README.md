# Rate My Recipe

## Project Overview

Rate My Recipe is a Python-based data analysis project that
investigates how recipes can be ranked using user ratings.

Ranking recipes solely by their average rating can be misleading,
especially when the number of ratings varies significantly.

This project introduces a weighted ranking strategy that combines
rating quality with the amount of available user feedback.

The project includes a Jupyter Notebook for statistical analysis
and an interactive Streamlit dashboard for exploring recipe rankings.

## Dataset

The project uses the Food.com Recipes and User Interactions dataset
available on Kaggle.

[Download the dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

The dataset contains:

- 231,637 recipes
- 1,132,367 user interactions
- 1,071,520 valid ratings
- 226,590 recipes with valid ratings

Download the following files and place them in `data/raw/`:

- RAW_recipes.csv
- RAW_interactions.csv

Raw datasets are excluded from the GitHub repository.

## Project Structure

```text
rate-my-recipe/
├── data/
│   └── raw/
│       ├── RAW_recipes.csv
│       └── RAW_interactions.csv
├── src/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── ranking.py
│   ├── analysis.py
│   └── plots.py
├── Python Project.ipynb
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Methodology

### 1. Data Processing

- Load recipe and interaction datasets.
- Check for missing files and duplicate records.
- Convert zero ratings to missing values.
- Aggregate valid ratings by recipe ID.
- Merge rating statistics with recipe characteristics.

### 2. Naive Ranking

Recipes are ranked according to their average rating.
This approach does not account for the number of ratings.

### 3. Weighted Ranking

The weighted rating is calculated as:

$$
WR = \frac{vR + mC}{v+m}
$$

Where:

- R: average rating of the recipe
- v: number of valid ratings
- C: global average rating
- m: weighting parameter

Recipes with fewer ratings are pulled toward the global
average, while recipes with more ratings rely more heavily
on their own average.

### 4. Sensitivity Analysis

Three weighting parameters were evaluated using the
distribution of valid rating counts:

| Percentile | Weighting parameter |
|---|---:|
| 90th | 9 |
| 95th | 14 |
| 99th | 45 |

The 95th percentile (m = 14) was selected as a balanced
weighting parameter for the final ranking.

### 5. Ingredient Category Analysis

Recipes are divided into three categories:

| Category | Number of ingredients |
|---|---:|
| Simple | 1–5 |
| Moderate | 6–10 |
| Complex | 11+ |

Category-level statistics and category-specific rankings
are calculated using Pandas.

## Performance Optimization and Validation

The original row-wise Pandas implementation was replaced
with a vectorized NumPy implementation.

A benchmark performed on 226,590 recipes produced the
following results:

| Implementation | Execution time |
|---|---:|
| Pandas Apply | 0.7797 seconds |
| NumPy Vectorization | 0.0192 seconds |

The vectorized implementation was approximately 40.5 times
faster in this benchmark.

Numerical equivalence was verified using `np.allclose()`.
Additional controlled test cases were used to validate
the weighted rating formula.

All controlled validation tests passed.

Execution times may vary depending on hardware and
environment.

## Key Findings

- The median number of valid ratings per recipe is only 2.
- The global average rating is approximately 4.66.
- Weighted ranking reduces the influence of extreme
  ratings based on small samples.
- The top 100 ranked recipes have the same median
  preparation time as the overall dataset: 40 minutes.
- Top-ranked recipes have fewer ingredients at the median.
- All three ingredient categories have a median weighted
  score of 4.6841, rounded to four decimal places.

These findings are descriptive and do not establish
causal relationships or predictive performance.

## Interactive Dashboard

The Streamlit dashboard allows users to:

- Switch between average and weighted ranking.
- Filter recipes by ingredient category.
- Adjust the weighting parameter.
- Select the number of displayed recipes.
- Explore rating distributions and relationships.

The dashboard reuses the same Python modules as the
Jupyter Notebook and uses caching to avoid repeatedly
loading the raw datasets.

## Installation

The project was developed using Python 3.12.7.

Clone the repository:

```bash
git clone https://github.com/MetinVs/rate-my-recipe.git
cd rate-my-recipe
```

Create a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

Download the datasets and place them in `data/raw/`
before running the project.

## Running the Project

### Jupyter Notebook

```bash
python -m jupyterlab
```

Open `Python Project.ipynb` and run all cells.

### Streamlit Dashboard

```bash
python -m streamlit run app.py
```

Open the local Streamlit address in your browser.

## Limitations

- The weighting parameter is a modeling choice rather
  than an empirically optimized parameter.
- Rating volume does not necessarily guarantee recipe quality.
- User-specific preferences are not considered.
- Ingredient count is only an approximate indicator
  of recipe complexity.
- The ranking has not been evaluated against future ratings.

## Author

Metin Mirza Vatansever

MSc Data Science for Economics and Health
University of Milan

Coding for Data Science and Data Management
Academic Year 2026/2027