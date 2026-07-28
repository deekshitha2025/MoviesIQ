import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Movie Revenue Analysis Dashboard",
    page_icon="🎬",
    layout="wide"
)
st.title("🎬 Movie Revenue Analysis Dashboard")

st.write("Analyze movie revenue, budget, popularity, genres and ratings.")
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
df = pd.read_csv(BASE_DIR / "movies.csv")
st.subheader("Dataset")

st.dataframe(df)
st.write(df.columns)
df = df.drop_duplicates()
df = df[df["budget"] >= 0]

df = df[df["revenue"] >= 0]
st.sidebar.title("Movie Filters")
genre = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + list(df["genres"].unique())
)
if genre != "All":
    df = df[df["genres"] == genre]
    budget = st.sidebar.slider(
    "Budget",
    int(df["budget"].min()),
    int(df["budget"].max()),
    (
        int(df["budget"].min()),
        int(df["budget"].max())
    )
)
    df = df[
    (df["budget"] >= budget[0]) &
    (df["budget"] <= budget[1])
]
    rating = st.sidebar.slider(
    "Minimum Rating",
    0.0,
    10.0,
    0.0
)
    df = df[df["vote_average"] >= rating]
    st.subheader("Filtered Dataset")

st.dataframe(df)
total_movies = len(df)

average_budget = df["budget"].mean()

average_revenue = df["revenue"].mean()

average_rating = df["vote_average"].mean()
col1,col2,col3,col4 = st.columns(4)
col1.metric(
    "Total Movies",
    total_movies
)
col2.metric(
    "Average Budget",
    f"${average_budget:,.0f}"
)
col3.metric(
    "Average Revenue",
    f"${average_revenue:,.0f}"
)
col4.metric(
    "Average Rating",
    round(average_rating,2)
)
top_movies = df.sort_values(
    "revenue",
    ascending=False
).head(10)
fig = px.bar(
    top_movies,
    x="title",
    y="revenue",
    color="revenue",
    title="Top 10 Revenue Movies"
)

st.plotly_chart(fig, use_container_width=True)
genre_data = df.groupby("genres")["revenue"].mean().reset_index()
fig = px.bar(
    genre_data,
    x="genres",
    y="revenue",
    color="revenue",
    title="Revenue by Genre"
)

st.plotly_chart(fig, use_container_width=True)
fig = px.scatter(
    df,
    x="budget",
    y="revenue",
    color="genres",
    hover_name="title",
    title="Budget vs Revenue"
)

st.plotly_chart(fig, use_container_width=True)
fig = px.scatter(
    df,
    x="popularity",
    y="revenue",
    color="genres",
    hover_name="title",
    title="Popularity vs Revenue"
)

st.plotly_chart(fig, use_container_width=True)
fig = px.histogram(
    df,
    x="runtime",
    nbins=30,
    title="Runtime Distribution"
)

st.plotly_chart(fig, use_container_width=True)
fig = px.histogram(
    df,
    x="vote_average",
    nbins=20,
    title="Rating Distribution"
)

st.plotly_chart(fig, use_container_width=True)
st.header("Business Insights")

st.success("""
• Action and Adventure movies generate high revenue.

• High-budget movies generally earn more revenue.

• Popular movies tend to generate higher revenue.

• Highly rated movies attract larger audiences.

• Some low-budget movies are also highly profitable.
""")
st.header("Business Recommendations")

st.info("""
• Invest more in profitable genres.

• Plan budgets using historical performance.

• Increase marketing for popular movies.

• Study successful low-budget movies.

• Produce high-quality movies to improve ratings.
""")
st.markdown("---")

st.caption("Developed using Streamlit | Pandas | Plotly")
