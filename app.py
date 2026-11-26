from pathlib import Path

import streamlit as st
import matplotlib.pyplot as plt

from src.data_processing import (
    load_data,
    clean_interactions,
    build_recipe_stats
)
from src.ranking import add_weighted_score, rank_recipes
from src.analysis import categorize_recipes
from src.plots import (
    plot_rating_distribution,
    plot_rating_relationship
)


st.set_page_config(
    page_title="Rate My Recipe",
    page_icon="🍝",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


@st.cache_data
def prepare_data():
    """Load, clean and prepare the recipe dataset."""

    recipes, interactions = load_data(RAW_DATA_DIR)

    interactions_clean = clean_interactions(interactions)

    recipe_stats = build_recipe_stats(
        recipes,
        interactions_clean
    )

    global_mean = interactions_clean["rating"].mean()

    return recipe_stats, global_mean


try:
    recipe_stats, C = prepare_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()


st.title("🍝 Rate My Recipe")

st.markdown(
    "Discover highly rated recipes using both "
    "rating quality and the number of user ratings."
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Recipes", f"{len(recipe_stats):,}")

col2.metric(
    "Valid Ratings",
    f"{int(recipe_stats['n_ratings'].sum()):,}"
)

col3.metric("Global Average Rating", f"{C:.3f}")
# Dashboard filters

st.sidebar.header("Ranking Settings")

ranking_method = st.sidebar.radio(
    "Ranking Method",
    ["Weighted Rating", "Average Rating"]
)

ingredient_category = st.sidebar.selectbox(
    "Ingredient Category",
    ["All Recipes", "Simple", "Moderate", "Complex"]
)

m = st.sidebar.slider(
    "Weighting Parameter (m)",
    min_value=0,
    max_value=100,
    value=14,
    step=1,
    disabled=(ranking_method == "Average Rating")
)

top_n = st.sidebar.slider(
    "Number of Recipes",
    min_value=5,
    max_value=100,
    value=10,
    step=5
)

st.sidebar.caption(
    "Higher m values pull ratings from small samples "
    "more strongly toward the global average."
)

# Calculate ranking scores

valid_recipes = recipe_stats.loc[
    recipe_stats["n_ratings"] > 0
].copy()

if ranking_method == "Weighted Rating":
    ranked_data = add_weighted_score(
        valid_recipes,
        global_mean=C,
        min_ratings=m,
        column_name="final_score"
    )
else:
    ranked_data = valid_recipes.copy()
    ranked_data["final_score"] = ranked_data["avg_rating"]


# Categorize and filter recipes

ranked_data = categorize_recipes(ranked_data)

if ingredient_category != "All Recipes":
    ranked_data = ranked_data.loc[
        ranked_data["ingredient_category"] == ingredient_category
    ]


# Create the final ranking

ranking_table = rank_recipes(
    ranked_data,
    "final_score"
).head(top_n)


# Display the results

st.subheader("Top-Ranked Recipes")

st.caption(
    f"{len(ranked_data):,} eligible recipes | "
    f"Ranking method: {ranking_method}"
)

display_table = ranking_table[
    [
        "name",
        "ingredient_category",
        "n_ingredients",
        "avg_rating",
        "n_ratings",
        "final_score"
    ]
].copy()

display_table.columns = [
    "Recipe",
    "Category",
    "Ingredients",
    "Average Rating",
    "Number of Ratings",
    "Ranking Score"
]

display_table = display_table.round(4)

display_table.index = range(1, len(display_table) + 1)

st.dataframe(display_table, width="stretch")

# Display rating visualizations

st.divider()

st.subheader("Rating Distribution and Reliability")

st.caption(
    "These visualizations describe the full dataset, "
    "independently of the selected ranking filters."
)

valid_rating_counts = recipe_stats.loc[
    recipe_stats["n_ratings"] > 0,
    "n_ratings"
]

review_limit = valid_rating_counts.quantile(0.99)

chart1, chart2 = st.columns(2)

with chart1:
    fig1 = plot_rating_distribution(
        recipe_stats,
        review_limit
    )
    st.pyplot(fig1)
    st.caption(
        "Rating count distribution up to the 99th percentile."
    )

with chart2:
    fig2 = plot_rating_relationship(recipe_stats)
    st.pyplot(fig2)
    st.caption(
        "Relationship between average rating and rating volume."
    )

st.info(
    "Most recipes receive relatively few ratings. "
    "Weighted ranking reduces the influence of "
    "extreme ratings based on small samples."
)
plt.close(fig1)
plt.close(fig2)
