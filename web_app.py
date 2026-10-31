import streamlit as st
import requests
import pandas as pd
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

# Load API Key
try:
    OMDB_API_KEY = st.secrets["OMDB_API_KEY"]
except Exception:
    OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")


# Fetch Movie Poster
def get_movie_poster(title):

    if not OMDB_API_KEY:
        return None

    try:
        url = "https://www.omdbapi.com/"

        params = {
            "apikey": OMDB_API_KEY,
            "t": title
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("Response") == "True":
            poster = data.get("Poster")

            if poster and poster != "N/A":
                return poster

        return None

    except requests.RequestException:
        return None

    except requests.RequestException:
        return None
# Custom Design
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #050816, #101b35, #172b4d);
    color: white;
}

h1 {
    color: #00d4ff !important;
    text-align: center;
    font-size: 45px;
    font-weight: 800;
}

h2, h3, p, label {
    color: white !important;
}

div.stButton > button {
    background: linear-gradient(90deg, #0077ff, #00d4ff);
    color: white !important;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    box-shadow: 0 0 15px #00d4ff;
}
</style>
""", unsafe_allow_html=True)

# Load Dataset
movies = pd.read_csv(
    Path(__file__).resolve().parent / "movies.csv",
    encoding="utf-8-sig"
)
movies = movies.reset_index(drop=True)

# AI Recommendation Model
movies["features"] = (
    movies["genre"].fillna("") + " " +
    movies["description"].fillna("")
)

vectorizer = TfidfVectorizer(stop_words="english")
feature_matrix = vectorizer.fit_transform(movies["features"])
similarity = cosine_similarity(feature_matrix)

# Website Heading
st.markdown("""
<h1 style='text-align:center; color:#00D4FF;'>
    🎬 WELCOME TO CINE AI
</h1>
<p style='text-align:center; font-size:18px;'>
    Discover Movies You'll Love ❤️
</p>
""", unsafe_allow_html=True)

st.divider()


# Search Movie
# Top Rated Movies
st.subheader("⭐ Top Rated Movies")

top_movies = movies.sort_values(
    by="rating",
    ascending=False
).head(5)

for index, movie in top_movies.iterrows():
   st.write(f"🎬 {movie['title']} — ⭐ {movie['rating']}/5")
# Genre Filter
st.subheader("🎭 Filter by Genre")

genres = ["All Genres"] + sorted(
    movies["genre"].dropna().unique().tolist()
)

selected_genre = st.selectbox(
    "Choose Genre",
    genres
)

# Search Movie
search_text = st.text_input("🔍 Search Movie")

filtered_movies = movies.copy()

if selected_genre != "All Genres":
    filtered_movies = filtered_movies[
        filtered_movies["genre"] == selected_genre
    ]

if search_text:
    filtered_movies = filtered_movies[
        filtered_movies["title"].str.contains(
            search_text, case=False, na=False
        )
    ]

matching_movies = filtered_movies["title"].tolist()

if not matching_movies:
    st.warning("No movie found. Try another name.")
    st.stop()

# Movie Selection

placeholder = "-- Select a Movie --"

if "movie_choice" not in st.session_state:
    st.session_state.movie_choice = placeholder

if st.session_state.movie_choice not in [placeholder] + matching_movies:
    st.session_state.movie_choice = placeholder

def clear_selection():
    st.session_state.movie_choice = placeholder

st.button(
    "❌ Clear Selection",
    on_click=clear_selection
)

selected_movie = st.selectbox(
    "Select a Movie",
    [placeholder] + matching_movies,
    key="movie_choice"
)

if selected_movie == placeholder:
    st.info("Please select a movie to see details.")
    st.stop()

# Movie Details
movie_info = movies[
    movies["title"] == selected_movie
].iloc[0]

st.subheader("🎥 Movie Details")
# Display Movie Poster
poster_url = get_movie_poster(selected_movie)

if poster_url:
    st.image(poster_url, width=250)
else:
    st.info("Movie poster not available.")

st.write("**Title:**", movie_info["title"])
st.write("**Genre:**", movie_info["genre"])
st.write("**Rating:**", str(movie_info["rating"]) + "/5")
st.write("**Description:**", movie_info["description"])

st.divider()
# Recommendation Button
if st.button("🎬 Recommend Movies"):

    movie_index = movie_info.name
    selected_genre = str(movie_info["genre"]).lower()

    scores = []

    for index in range(len(movies)):

        if index == movie_index:
            continue

        other_genre = str(movies.iloc[index]["genre"]).lower()

        genre_match = 1 if selected_genre == other_genre else 0

        similarity_score = similarity[movie_index][index]

        rating_score = float(movies.iloc[index]["rating"]) / 5

        final_score = (
            genre_match * 0.5
            + similarity_score * 0.3
            + rating_score * 0.2
        )

        scores.append((index, final_score))

    scores.sort(key=lambda item: item[1], reverse=True)

    st.subheader("⭐ Recommended Movies")

    count = 0

    for index, score in scores:

        if score < 0.25:
            continue

        movie = movies.iloc[index]

        poster = get_movie_poster(movie["title"])

        col1, col2 = st.columns([1, 2])

        with col1:
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.write("🎬 Poster unavailable")

        with col2:
            st.markdown(f"### 🎬 {movie['title']}")
            st.write(f"⭐ Rating: {movie['rating']}/5")
            st.write(f"🎭 Genre: {movie['genre']}")
            st.write(movie["description"])

        st.divider()
        count += 1

        if count == 5:
            break

    if count == 0:
        st.info("No similar movies found.")
        # About Us Section
st.divider()

st.markdown("""
<h2 style='text-align:center; color:#00D4FF;'>
    ℹ️ About Us
</h2>

<p style='text-align:center; font-size:17px;'>
    AI Movie Recommender is an intelligent movie recommendation
    platform that helps users discover movies they may love.
    It uses Machine Learning to suggest similar movies.
</p>
""", unsafe_allow_html=True)
# Footer Section
st.markdown("""
<hr>

<div style='text-align:center; color:#BBBBBB; padding:15px;'>

    <h3 style='color:#00D4FF;'>🎬 CINE AI</h3>

    <p>Discover Movies You'll Love ❤️</p>

    <p>Developed as an AI Movie Recommendation Project</p>

    <p>© 2026 CINE AI | All Rights Reserved</p>

</div>
""", unsafe_allow_html=True)