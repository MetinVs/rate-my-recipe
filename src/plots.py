import matplotlib.pyplot as plt
import seaborn as sns


def plot_rating_distribution(recipe_stats, review_limit):
    """Plot rating counts up to the selected percentile.

    Parameters
    ----------
    recipe_stats : pandas.DataFrame
        Recipe-level dataset containing rating counts.
    review_limit : float
        Upper rating count limit for visualization.

    Returns
    -------
    matplotlib.figure.Figure
        Histogram of rating counts.
    """

    data = recipe_stats.loc[
        recipe_stats["n_ratings"].between(1, review_limit),
        "n_ratings"
    ]

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.histplot(
        data,
        bins=int(review_limit),
        ax=ax
    )

    ax.set_title("Distribution of Number of Ratings per Recipe")
    ax.set_xlabel("Number of Ratings")
    ax.set_ylabel("Number of Recipes")

    fig.tight_layout()

    return fig

def plot_rating_relationship(recipe_stats):
    """Plot average ratings against valid rating counts.

    Parameters
    ----------
    recipe_stats : pandas.DataFrame
        Recipe-level dataset containing rating statistics.

    Returns
    -------
    matplotlib.figure.Figure
        Scatter plot of rating counts and average ratings.
    """

    data = recipe_stats.loc[
        (recipe_stats["n_ratings"] > 0)
        & recipe_stats["avg_rating"].notna()
    ]

    fig, ax = plt.subplots(figsize=(9, 6))

    sns.scatterplot(
        data=data,
        x="n_ratings",
        y="avg_rating",
        alpha=0.20,
        s=20,
        ax=ax
    )

    ax.set_xscale("log")
    ax.set_title("Average Rating vs Number of Ratings")
    ax.set_xlabel("Number of Ratings (Log Scale)")
    ax.set_ylabel("Average Rating")

    fig.tight_layout()

    return fig