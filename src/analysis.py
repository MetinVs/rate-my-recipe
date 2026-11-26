import numpy as np
import pandas as pd


def categorize_recipes(recipe_stats):
    """Categorize recipes based on their ingredient count.

    Parameters
    ----------
    recipe_stats : pandas.DataFrame
        Recipe-level dataset containing ingredient counts.

    Returns
    -------
    pandas.DataFrame
        Dataset with an additional ingredient_category column.
    """

    result = recipe_stats.copy()

    result["ingredient_category"] = pd.cut(
        result["n_ingredients"],
        bins=[0, 5, 10, np.inf],
        labels=["Simple", "Moderate", "Complex"]
    )

    return result

def summarize_categories(recipe_stats):
    """Calculate summary statistics for each ingredient category.

    Parameters
    ----------
    recipe_stats : pandas.DataFrame
        Categorized recipe dataset containing rating statistics.

    Returns
    -------
    pandas.DataFrame
        Summary statistics for each ingredient category.
    """

    return (
        recipe_stats
        .groupby("ingredient_category", observed=True)
        .agg(
            recipe_count=("id", "count"),
            median_rating=("avg_rating", "median"),
            median_weighted_score=("final_score", "median"),
            median_rating_count=("n_ratings", "median")
        )
        .round(4)
    )

def top_recipes_by_category(recipe_stats, n=5):
    """Return the highest-ranked recipes within each category.

    Parameters
    ----------
    recipe_stats : pandas.DataFrame
        Categorized recipe dataset containing weighted scores.
    n : int, default 5
        Number of recipes to return per category.

    Returns
    -------
    pandas.DataFrame
        Top-ranked recipes for each ingredient category.
    """

    return (
        recipe_stats
        .sort_values("final_score", ascending=False)
        .groupby("ingredient_category", observed=True)
        .head(n)
        .sort_values(
            ["ingredient_category", "final_score"],
            ascending=[True, False]
        )
    )