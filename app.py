# ============================================================
# 🎬 MOVIE REVENUE ANALYSIS DASHBOARD
# PART 1 - IMPORTS, CSS, DATA LOADING & SIDEBAR
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="🎬 Movie Revenue Dashboard",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family:Arial;
}

.main{
    background:#F4F7FC;
}

.block-container{
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0F172A,#1E3A8A);
}

[data-testid="stSidebar"] *{
    color:white;
}

.card{
    border-radius:18px;
    padding:20px;
    color:white;
    text-align:center;
    box-shadow:0px 5px 20px rgba(0,0,0,.20);
}

.chart{
    background:white;
    border-radius:18px;
    padding:10px;
    box-shadow:0px 5px 15px rgba(0,0,0,.12);
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.markdown("""
<div style="
background:linear-gradient(90deg,#2563EB,#9333EA);
padding:30px;
border-radius:20px;
color:white;
text-align:center;
">

<h1>🎬 Movie Revenue Analysis Dashboard</h1>

<h4>
Business Intelligence Dashboard using Streamlit & Plotly
</h4>

</div>
""", unsafe_allow_html=True)

st.write("")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

BASE_DIR = Path(__file__).parent

df = pd.read_csv(BASE_DIR / "movies.csv")

# ------------------------------------------------------------
# CLEAN DATA
# ------------------------------------------------------------

df.drop_duplicates(inplace=True)

df = df[df["budget"] >= 0]

df = df[df["revenue"] >= 0]

df["genres"] = df["genres"].fillna("Unknown")

df["title"] = df["title"].fillna("Unknown")

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/4221/4221419.png",
    width=120
)

st.sidebar.title("🎯 Dashboard Filters")

# Genre

genres = ["All"] + sorted(df["genres"].unique())

selected_genre = st.sidebar.selectbox(
    "Genre",
    genres
)

# Rating

selected_rating = st.sidebar.slider(
    "Minimum Rating",
    0.0,
    10.0,
    0.0,
    0.1
)

# Budget

selected_budget = st.sidebar.slider(
    "Budget Range",

    int(df["budget"].min()),

    int(df["budget"].max()),

    (
        int(df["budget"].min()),
        int(df["budget"].max())
    )
)

# Runtime

selected_runtime = st.sidebar.slider(

    "Runtime",

    int(df["runtime"].min()),

    int(df["runtime"].max()),

    (
        int(df["runtime"].min()),
        int(df["runtime"].max())
    )

)

# Search Movie

movie_search = st.sidebar.text_input(
    "🔍 Search Movie"
)

# ------------------------------------------------------------
# APPLY FILTERS
# ------------------------------------------------------------

filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["genres"] == selected_genre
    ]

filtered_df = filtered_df[
    filtered_df["vote_average"] >= selected_rating
]

filtered_df = filtered_df[
    (filtered_df["budget"] >= selected_budget[0]) &
    (filtered_df["budget"] <= selected_budget[1])
]

filtered_df = filtered_df[
    (filtered_df["runtime"] >= selected_runtime[0]) &
    (filtered_df["runtime"] <= selected_runtime[1])
]

if movie_search != "":
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(
            movie_search,
            case=False,
            na=False
        )
    ]

# ------------------------------------------------------------
# DATASET PREVIEW
# ------------------------------------------------------------

st.subheader("📂 Movie Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=300
)

# ------------------------------------------------------------
# KPI VALUES
# ------------------------------------------------------------

total_movies = len(filtered_df)

average_budget = filtered_df["budget"].mean()

average_revenue = filtered_df["revenue"].mean()

average_rating = filtered_df["vote_average"].mean()

highest_movie = filtered_df.sort_values(
    "revenue",
    ascending=False
).iloc[0]["title"] if len(filtered_df)>0 else "N/A"
# ============================================================
# PART 2 - KPI CARDS
# ============================================================

st.write("")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#2563EB,#1D4ED8);">
        <h4>🎬 Total Movies</h4>
        <h1>{total_movies}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#10B981,#059669);">
        <h4>💰 Avg Revenue</h4>
        <h2>${average_revenue:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#8B5CF6,#7C3AED);">
        <h4>💵 Avg Budget</h4>
        <h2>${average_budget:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#F59E0B,#D97706);">
        <h4>⭐ Avg Rating</h4>
        <h2>{average_rating:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("---")

# ============================================================
# TOP 10 REVENUE MOVIES
# ============================================================

left, right = st.columns(2)

with left:

    st.subheader("🏆 Top 10 Revenue Movies")

    top_movies = (
        filtered_df
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        top_movies,
        x="title",
        y="revenue",
        color="revenue",
        text="revenue",
        template="plotly_white",
        color_continuous_scale="Blues"
    )

    fig1.update_layout(
        xaxis_title="Movie",
        yaxis_title="Revenue",
        height=500
    )

    st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# REVENUE BY GENRE
# ============================================================

with right:

    st.subheader("💰 Average Revenue by Genre")

    genre_rev = (
        filtered_df
        .groupby("genres")["revenue"]
        .mean()
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    fig2 = px.bar(
        genre_rev,
        x="genres",
        y="revenue",
        color="revenue",
        text_auto=".2s",
        template="plotly_white",
        color_continuous_scale="Viridis"
    )

    fig2.update_layout(height=500)

    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# GENRE DISTRIBUTION
# ============================================================

left, right = st.columns(2)

with left:

    st.subheader("🎭 Genre Distribution")

    genre_count = (
        filtered_df["genres"]
        .value_counts()
        .reset_index()
    )

    genre_count.columns = ["Genre", "Count"]

    fig3 = px.pie(
        genre_count,
        names="Genre",
        values="Count",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig3.update_layout(height=450)

    st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# HIGHEST RATED MOVIES
# ============================================================

with right:

    st.subheader("⭐ Highest Rated Movies")

    rating_df = (
        filtered_df
        .sort_values("vote_average", ascending=False)
        .head(10)
    )

    fig4 = px.bar(
        rating_df,
        x="title",
        y="vote_average",
        color="vote_average",
        text="vote_average",
        template="plotly_white",
        color_continuous_scale="Sunset"
    )

    fig4.update_layout(height=450)

    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
# ============================================================
# PART 3 - ADVANCED VISUALIZATIONS
# ============================================================

st.header("📊 Advanced Analytics")

# ------------------------------------------------------------
# Budget vs Revenue
# ------------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("💰 Budget vs Revenue")

    fig5 = px.scatter(
        filtered_df,
        x="budget",
        y="revenue",
        color="genres",
        size="vote_average",
        hover_name="title",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig5.update_layout(height=500)

    st.plotly_chart(fig5, use_container_width=True)

# ------------------------------------------------------------
# Popularity vs Revenue
# ------------------------------------------------------------

with right:

    st.subheader("🔥 Popularity vs Revenue")

    fig6 = px.scatter(
        filtered_df,
        x="popularity",
        y="revenue",
        color="genres",
        hover_name="title",
        size="vote_average",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    fig6.update_layout(height=500)

    st.plotly_chart(fig6, use_container_width=True)

# ============================================================
# Runtime Distribution
# ============================================================

left, right = st.columns(2)

with left:

    st.subheader("⏱ Runtime Distribution")

    fig7 = px.histogram(
        filtered_df,
        x="runtime",
        nbins=30,
        color_discrete_sequence=["#2563EB"],
        template="plotly_white"
    )

    fig7.update_layout(height=450)

    st.plotly_chart(fig7, use_container_width=True)

# ============================================================
# Rating Distribution
# ============================================================

with right:

    st.subheader("⭐ Rating Distribution")

    fig8 = px.histogram(
        filtered_df,
        x="vote_average",
        nbins=20,
        color_discrete_sequence=["#F59E0B"],
        template="plotly_white"
    )

    fig8.update_layout(height=450)

    st.plotly_chart(fig8, use_container_width=True)

# ============================================================
# Revenue by Runtime
# ============================================================

left, right = st.columns(2)

with left:

    st.subheader("📈 Revenue vs Runtime")

    fig9 = px.scatter(
        filtered_df,
        x="runtime",
        y="revenue",
        color="genres",
        hover_name="title",
        template="plotly_white"
    )

    fig9.update_layout(height=450)

    st.plotly_chart(fig9, use_container_width=True)

# ============================================================
# Budget Distribution
# ============================================================

with right:

    st.subheader("💵 Budget Distribution")

    fig10 = px.box(
        filtered_df,
        y="budget",
        color="genres",
        template="plotly_white"
    )

    fig10.update_layout(height=450)

    st.plotly_chart(fig10, use_container_width=True)

# ============================================================
# Correlation Heatmap
# ============================================================

st.subheader("📌 Correlation Heatmap")

corr = filtered_df[
    [
        "budget",
        "revenue",
        "popularity",
        "runtime",
        "vote_average"
    ]
].corr()

fig11 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    aspect="auto"
)

fig11.update_layout(height=500)

st.plotly_chart(fig11, use_container_width=True)

# ============================================================
# Top 15 Popular Movies
# ============================================================

st.subheader("🌟 Top 15 Most Popular Movies")

popular_movies = (
    filtered_df
    .sort_values("popularity", ascending=False)
    .head(15)
)

fig12 = px.bar(
    popular_movies,
    x="title",
    y="popularity",
    color="popularity",
    template="plotly_white",
    color_continuous_scale="Turbo"
)

fig12.update_layout(height=500)

st.plotly_chart(fig12, use_container_width=True)

st.markdown("---")
# ============================================================
# PART 4 - BUSINESS INSIGHTS
# ============================================================

st.header("📈 Business Insights")

highest_revenue_movie = filtered_df.loc[
    filtered_df["revenue"].idxmax(), "title"
]

highest_rated_movie = filtered_df.loc[
    filtered_df["vote_average"].idxmax(), "title"
]

most_popular_movie = filtered_df.loc[
    filtered_df["popularity"].idxmax(), "title"
]

best_genre = (
    filtered_df.groupby("genres")["revenue"]
    .mean()
    .idxmax()
)

average_runtime = filtered_df["runtime"].mean()

st.markdown(f"""
<div style="
background:white;
padding:25px;
border-radius:20px;
box-shadow:0px 5px 15px rgba(0,0,0,.15);
">

<h3>📊 Key Findings</h3>

<ul>

<li>🎬 Total Movies Analysed :
<b>{total_movies}</b></li>

<li>💰 Highest Revenue Movie :
<b>{highest_revenue_movie}</b></li>

<li>⭐ Highest Rated Movie :
<b>{highest_rated_movie}</b></li>

<li>🔥 Most Popular Movie :
<b>{most_popular_movie}</b></li>

<li>🏆 Best Performing Genre :
<b>{best_genre}</b></li>

<li>⏱ Average Runtime :
<b>{average_runtime:.1f} minutes</b></li>

</ul>

</div>
""", unsafe_allow_html=True)

st.write("")

# ============================================================
# BUSINESS RECOMMENDATIONS
# ============================================================

st.header("💡 Business Recommendations")

col1, col2 = st.columns(2)

with col1:

    st.success("""
### 🎯 Investment Strategy

✅ Invest more in high-performing genres.

✅ Allocate higher budgets to proven genres.

✅ Study successful low-budget films.

✅ Improve production quality.

✅ Analyze audience preferences.
""")

with col2:

    st.info("""
### 📢 Marketing Strategy

📌 Increase marketing for highly popular movies.

📌 Improve social media campaigns.

📌 Release trailers earlier.

📌 Focus on audience ratings.

📌 Target family and action audiences.
""")

st.write("")

# ============================================================
# TOP MOVIE SUMMARY
# ============================================================

st.header("🏆 Top Movie Summary")

summary = filtered_df[
    [
        "title",
        "genres",
        "budget",
        "revenue",
        "vote_average",
        "popularity"
    ]
].sort_values(
    "revenue",
    ascending=False
)

st.dataframe(
    summary.head(20),
    use_container_width=True
)

# ============================================================
# DOWNLOAD BUTTON
# ============================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="Filtered_Movies.csv",
    mime="text/csv"
)

# ============================================================
# ABOUT PROJECT
# ============================================================

st.markdown("---")

st.header("🎬 About Project")

st.write("""

The **Movie Revenue Analysis Dashboard** helps production
companies understand how budget, popularity,
ratings and genres influence movie revenue.

The dashboard enables users to

• Filter movies

• Analyze revenue

• Explore genres

• Compare budgets

• Study popularity

• Generate business insights

• Support data-driven decisions

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown(
"""
<hr>

<center>

<h4>
🎬 Movie Revenue Analysis Dashboard
</h4>

Built using ❤️ Streamlit | Pandas | Plotly

Created by **Deekshitha**

</center>

""",
unsafe_allow_html=True
)
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Dashboard",
        "📈 Analytics",
        "💡 Insights",
        "ℹ️ About"
    ]
)