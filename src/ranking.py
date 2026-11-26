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
    recipe_stats,
    global_mean,
    min_ratings,
    column_name="weighted_score"
):
    """Calculate weighted recipe scores using vectorization."""

    result = recipe_stats.copy()

    mask = result["n_ratings"] > 0

    R = result.loc[mask, "avg_rating"].to_numpy()
    v = result.loc[mask, "n_ratings"].to_numpy()

    scores = (
        v * R + min_ratings * global_mean
    ) / (v + min_ratings)

    result[column_name] = np.nan
    result.loc[mask, column_name] = scores

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