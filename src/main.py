import pandas as pd
import pycountry
import streamlit as st

from src import APP_DIR

pycountry.countries.add_entry(
    alpha_2="XK", alpha_3="XXK", name="Kosovo", numeric="926", flag="🇽🇰"
)

st.set_page_config(page_title="Olympic medals", page_icon="🏅", layout="wide")


def get_data() -> pd.DataFrame:
    url = "https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table"

    html = pd.read_html(url, match="2024 Summer Olympics medal table")
    if len(html) != 1:
        raise ValueError(f"Did not found table in '{url}'")

    df = html[0]

    # remove last line
    df = df.iloc[:-1]

    return df


def rename_country(series: pd.Series) -> pd.Series:
    return series.replace("Great Britain", "United Kingdom").replace(
        "Turkey", "Türkiye"
    )


def enrich_country(df: pd.DataFrame) -> pd.DataFrame:
    df["country"] = rename_country(df["country"])
    df["country"] = (
        df["country"].str.replace("*", "").replace(" ", "-").replace("ROC", "Russia")
    )
    df["country_object"] = df["country"].map(
        lambda x: pycountry.countries.get(name=x)
        or pycountry.countries.get(common_name=x)
    )
    df["country_code"] = df["country_object"].map(lambda x: x.alpha_3 if x else None)
    df["country_flag"] = df["country_object"].map(lambda x: x.flag if x else None)
    df = df.drop(columns=["country_object"])
    return df


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(
        columns={
            "NOC": "country",
            "Gold": "gold",
            "Silver": "silver",
            "Bronze": "bronze",
            "Total": "total_medals",
            "Rank": "official_rank",
        }
    )

    # convert to integer
    df["gold"] = df["gold"].astype(int)
    df["silver"] = df["silver"].astype(int)
    df["bronze"] = df["bronze"].astype(int)
    df["total_medals"] = df["total_medals"].astype(int)
    df["official_rank"] = df["official_rank"].astype(int)

    df = enrich_country(df)

    return df


def compute_weighted_score(
    df: pd.DataFrame,
    weight_gold: int = 1,
    weight_silver: int = 1,
    weight_bronze: int = 1,
) -> pd.Series:
    return (
        df["gold"] * weight_gold
        + df["silver"] * weight_silver
        + df["bronze"] * weight_bronze
    )


def compute_new_rank(score: pd.Series) -> pd.Series:
    return score.rank(method="min", ascending=False).astype(int)


def get_new_rank_emoji(new_rank, official_rank):
    if new_rank < official_rank:
        return "⬆️"
    elif new_rank > official_rank:
        return "⬇️"
    else:
        return "🟰"


def recompute_rank(
    df: pd.DataFrame,
    weight_gold: int = 1,
    weight_silver: int = 1,
    weight_bronze: int = 1,
) -> pd.DataFrame:
    df["score"] = compute_weighted_score(df, weight_gold, weight_silver, weight_bronze)
    df = df.sort_values("score", ascending=False)
    df["new_rank"] = compute_new_rank(df["score"])
    df["new_rank_emoji"] = df.apply(
        lambda x: get_new_rank_emoji(x["new_rank"], x["official_rank"]), axis=1
    )
    df["progression"] = df["official_rank"] - df["new_rank"]
    df["country"] = df["country"] + " " + df["country_flag"]
    df = df.loc[
        :,
        [
            "country",
            "official_rank",
            "new_rank",
            "progression",
            "new_rank_emoji",
            "gold",
            "silver",
            "bronze",
            "total_medals",
            "score",
        ],
    ]
    return df


st.title("2024 Summer Olympics Medal Table")

st.subheader("Recompute the rank based on a weighted score of 🥇, 🥈 and 🥉.")

st.text("Play with the cursors on the left and see how it affects the rank.")

st.markdown("____")

df = get_data()
df = process_data(df)


def get_weight_param(param_name: str, default_value: int) -> int:
    try:
        return int(st.query_params.get(param_name, default_value))
    except Exception:
        return default_value


with st.sidebar:
    st.header("Weights")
    weight_gold = st.slider(
        "Weight for 🥇", 0, 20, get_weight_param("weight_gold", 10), 1
    )
    weight_silver = st.slider(
        "Weight for 🥈", 0, 20, get_weight_param("weight_silver", 5), 1
    )
    weight_bronze = st.slider(
        "Weight for 🥉", 0, 20, get_weight_param("weight_bronze", 1), 1
    )

if weight_gold < weight_silver:
    st.warning("Weight for Gold should be higher than Silver")
if weight_silver < weight_bronze:
    st.warning("Weight for Silver should be higher than Bronze")
if weight_gold < weight_bronze:
    st.warning("Weight for Gold should be higher than Bronze")

df = recompute_rank(df, weight_gold, weight_silver, weight_bronze)

small_column_width = 10
medium_column_width = 70

th_style = dict(
    selector="th",
    props=[
        ("text-align", "center"),
        ("font-size", "20em"),
    ],
)
td_style = dict(selector="td", props=[("text-align", "center")])

st.dataframe(
    df.style.set_table_styles(
        [
            th_style,
            td_style,
        ]
    )
    .background_gradient(subset=["progression"], cmap="RdYlGn", vmin=-10, vmax=10)
    .background_gradient(subset=["official_rank", "new_rank"], cmap="summer"),
    use_container_width=True,
    column_config={
        "country": st.column_config.TextColumn(label="Country", width=150),
        "official_rank": st.column_config.NumberColumn(
            label="Official Rank", width=medium_column_width
        ),
        "new_rank": st.column_config.NumberColumn(
            label="New Rank", width=medium_column_width
        ),
        "progression": st.column_config.NumberColumn(
            label="Progression", width=medium_column_width
        ),
        "new_rank_emoji": st.column_config.TextColumn(
            label="🚀", width=small_column_width
        ),
        "gold": st.column_config.NumberColumn(label="🥇", width=small_column_width),
        "silver": st.column_config.NumberColumn(label="🥈", width=small_column_width),
        "bronze": st.column_config.NumberColumn(label="🥉", width=small_column_width),
        "total_medals": st.column_config.NumberColumn(
            label="🏅", width=small_column_width
        ),
        "score": st.column_config.NumberColumn(label="Score", width=30),
    },
    hide_index=True,
)

with (APP_DIR / "about.md").open(mode="r") as f:
    about_markdown = f.read()

with st.expander("About"):
    st.markdown(about_markdown)
