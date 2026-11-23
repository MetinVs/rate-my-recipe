import numpy as np
import pandas as pd


def weighted_rating(
    row: pd.Series,
    global_mean: float,
    min_ratings: float
) -> float:
    """
    Calculate a weighted rating for one recipe.
    """
    R = row["avg_rating"]
    v = row["n_ratings"]

    return (
        (v / (v + min_ratings)) * R
        + (min_ratings / (v + min_ratings)) * global_mean
    )


def add_weighted_score(
    recipe_stats: pd.DataFrame,
    global_mean: float,
    min_ratings: float,
    column_name: str = "weighted_score"
) -> pd.DataFrame:
    """
    Add a weighted rating score to the recipe dataset.
    """
    result = recipe_stats.copy()

    result[column_name] = np.nan

    mask = result["n_ratings"] > 0

    result.loc[mask, column_name] = (
        result.loc[mask]
        .apply(
            weighted_rating,
            axis=1,
            global_mean=global_mean,
            min_ratings=min_ratings
        )
    )

    return result


def rank_recipes(
    recipe_stats: pd.DataFrame,
    score_column: str
) -> pd.DataFrame:
    """
    Rank recipes from highest to lowest score.
    """
    return (
        recipe_stats[
            recipe_stats[score_column].notna()
        ]
        .sort_values(
            score_column,
            ascending=False
        )
    )