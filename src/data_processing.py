from pathlib import Path

import numpy as np
import pandas as pd


def load_data(raw_data_dir: Path):
    """
    Load the Food.com recipe and interaction datasets.
    """
    recipes = pd.read_csv(raw_data_dir / "RAW_recipes.csv")
    interactions = pd.read_csv(raw_data_dir / "RAW_interactions.csv")

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