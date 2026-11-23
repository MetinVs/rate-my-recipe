# Rate My Recipe

## Project Overview

This project analyzes user ratings from the Food.com dataset to develop a more reliable method for ranking recipes.

A simple ranking based only on average ratings can be misleading. For example, a recipe with a 5.0 average rating based on only one review may appear above a recipe with a 4.9 average rating supported by hundreds of reviews.

The objective of this project is to create a ranking method that considers both:

- the average rating of a recipe;
- the number of ratings received.

## Dataset

The project uses the Food.com Recipes and User Interactions dataset.

Two main files are used:

- `RAW_recipes.csv` — recipe information such as preparation time, ingredients and number of steps;
- `RAW_interactions.csv` — user interactions containing recipe ratings and reviews.

The raw data files are stored locally inside:

```text
data/raw/
```

The raw data is not included in the GitHub repository because of its size.

## Project Structure

```text
Coding for Data Science and Data Management/
│
├── Python Project.ipynb
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── raw/
│
├── src/
│   ├── data_processing.py
│   └── ranking.py
│
└── outputs/
```

## Data Preparation

User interactions with a rating equal to `0` are treated as missing star ratings and are excluded from rating calculations.

The interaction data is then aggregated to recipe level to calculate:

- `avg_rating` — average valid rating;
- `n_ratings` — number of valid ratings received by each recipe.

These statistics are merged with the recipe dataset.

## Naive Ranking

The first ranking method orders recipes only by their average rating.

This approach reveals an important limitation: many recipes with a perfect 5.0 average rating have received only one or a few ratings.

Therefore, the raw average alone does not provide information about the reliability of the score.

## Weighted Rating

To account for the number of ratings, the project uses a weighted rating:

\[
WR =
\frac{v}{v+m}R +
\frac{m}{v+m}C
\]

where:

- `R` = average rating of the recipe;
- `v` = number of valid ratings received by the recipe;
- `C` = global average rating across all valid user ratings;
- `m` = confidence threshold.

Recipes with only a few ratings are pulled toward the global average, while recipes with many ratings depend more strongly on their own average rating.

## Confidence Threshold

The 90th, 95th and 99th percentiles of the rating-count distribution were tested as alternative confidence thresholds.

These correspond approximately to:

- 90th percentile: 9 ratings;
- 95th percentile: 14 ratings;
- 99th percentile: 45 ratings.

The 95th percentile (`m = 14`) was selected as the final threshold because it provides a balance between rating quality and rating volume without giving excessive importance only to the most-reviewed recipes.

## Main Findings

The dataset contains more than 230,000 recipes and more than one million user interactions.

The analysis shows that:

- most recipes receive relatively few ratings;
- raw average ratings are therefore sensitive to small sample sizes;
- the weighted ranking substantially reduces the influence of recipes supported by only one or a few ratings;
- highly ranked recipes have similar median preparation times to the overall recipe population;
- the top-ranked recipes tend to use slightly fewer ingredients.

## Requirements

The project uses:

- Python
- NumPy
- pandas
- Matplotlib
- Seaborn

Install the required packages with:

```bash
pip install -r requirements.txt
```

## Running the Project

1. Download the Food.com dataset.
2. Place `RAW_recipes.csv` and `RAW_interactions.csv` inside:

```text
data/raw/
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. Open and run:

```text
Python Project.ipynb
```

The notebook imports the data-processing and ranking functions from the `src` directory.

## Author

Metin Mirza Vatansever  
MSc Data Science for Economics and Health  
University of Milan