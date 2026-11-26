from pathlib import Path

import numpy as np
import pandas as pd


def load_data(raw_data_dir: Path):
    """Load recipe and interaction datasets from CSV files."""

    recipes_path = raw_data_dir / "RAW_recipes.csv"
    interactions_path = raw_data_dir / "RAW_interactions.csv"

    for path in [recipes_path, interactions_path]:
        if not path.is_file():
            raise FileNotFoundError(
                f"Dataset not found: {path}. "
                "Download the Food.com dataset from Kaggle "
                "and place the CSV files in data/raw/."
            )

    recipes = pd.read_csv(recipes_path)
    interactions = pd.read_csv(interactions_path)

    return recipes, interactions

def clean_interactions(interactions: pd.DataFrame) -> pd.DataFrame:
    """
    Convert rating 0 values into missing values.
    """
    cleaned = interactions.copy()
    cleaned["rating"] = cleaned["rating"].replace(0, np.nan)

    return cleaned


def build_recipe_stats(
    recipes: pd.DataFrame,
    interactions: pd.DataFrame
) -> pd.DataFrame:
    """
    Create one row per recipe with average rating and rating count.
    """
    rating_summary = (
        interactions
        .groupby("recipe_id")
        .agg(
            avg_rating=("rating", "mean"),
            n_ratings=("rating", "count")
        )
        .reset_index()
    )

    recipe_stats = recipes.merge(
        rating_summary,
        left_on="id",
        right_on="recipe_id",
        how="left"
    )

    recipe_stats.drop(columns="recipe_id", inplace=True)

    return recipe_stats