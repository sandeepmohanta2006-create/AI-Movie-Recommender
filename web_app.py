import streamlit as st
import requests
import pandas as pd
import os
import html
import textwrap
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
   page_title="Cine AI",
    page_icon="🎬",
    layout="centered"
)

# CINE AI - Mobile Poster Fix
st.markdown("""
<style>
@media screen and (max-width: 768px) {

    .netflix-row {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 10px !important;
    }

    .netflix-card img {
        width: 100% !important;
        height: 140px !important;
        object-fit: contain !important;
    }

    [data-testid="stImage"] img {
        width: 100% !important;
        height: 150px !important;
        object-fit: contain !important;
    }
}
/* Movie Card Hover Zoom Animation */

.netflix-card {
    transition: transform 0.35s ease, box-shadow 0.35s ease !important;
}

@media (hover: hover) {
    .netflix-card:hover {
        transform: scale(1.06) !important;
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.35) !important;
        z-index: 10;
    }
}
</style>
""", unsafe_allow_html=True)

# Load API Key
try:
    OMDB_API_KEY = st.secrets["OMDB_API_KEY"]
except Exception:
    OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")
# Load API Key
try:
    OMDB_API_KEY = st.secrets["OMDB_API_KEY"]
except Exception:
    OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")


# Fetch Movie Poster
@st.cache_data(ttl=86400)
def get_movie_poster(title):

    if not OMDB_API_KEY:
        return None

    try:
        url = "https://www.omdbapi.com/"

        params = {
            "apikey": OMDB_API_KEY,
            "t": title
        }

        if title.strip().lower() == "krrish":
            params["y"] = "2006"

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("Response") == "True":
            poster = data.get("Poster")

            if poster and poster != "N/A":
                return poster

        return None

    except requests.RequestException:
        return None

    # Fetch Complete Movie Details
@st.cache_data(ttl=86400)
def get_movie_details(title):

    if not OMDB_API_KEY:
        return None

    try:
        url = "https://www.omdbapi.com/"

        params = {
            "apikey": OMDB_API_KEY,
            "t": title,
            "plot": "full"
        }

        if title.strip().lower() == "krrish":
            params["y"] = "2006"

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("Response") == "True":
            return {
                "year": data.get("Year", "N/A"),
                "imdb_rating": data.get("imdbRating", "N/A"),
                "director": data.get("Director", "N/A"),
                "actors": data.get("Actors", "N/A"),
                "runtime": data.get("Runtime", "N/A"),
                "plot": data.get("Plot", "N/A"),
                "language": data.get("Language", "N/A"),
                "genre": data.get("Genre", "N/A")
            }

        return None

    except requests.RequestException:
        return None
## Custom Design
# Custom Design
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #050816, #101b35, #172b4d);
    color: white;
}

/* Main Heading */
h1 {
    color: #00d4ff !important;
    text-align: center;
    font-size: 45px;
    font-weight: 800;
}

/* Other Headings */
h2, h3, p, label {
    color: white !important;
}

/* Search Bar */
div[data-testid="stTextInput"] input {
    background-color: #172b4d;
    color: white !important;
    border: 1px solid #00d4ff;
    border-radius: 10px;
}

/* Dropdown */
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #172b4d;
    border-radius: 10px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #0077ff, #00d4ff);
    color: white !important;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease;
}

/* Button Hover */
div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 18px #00d4ff;
}




/* Sidebar Design */

[data-testid="stSidebar"] {
   background: linear-gradient(180deg, #050816, #101b35, #172b4d);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Sidebar Navigation */
[data-testid="stSidebarNav"] a {
    color: white !important;
    border-radius: 10px;
}


[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #0077ff !important;
}
/* Movie Card Hover */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 15px;
    transition: all 0.3s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border: 1px solid #00d4ff !important;
    box-shadow: 0 0 25px #00d4ff !important;
    transform: translateY(-5px);

}
/* CINE AI Sidebar Gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050816, #101b35, #172b4d) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

[data-testid="stSidebarNav"],
[data-testid="stSidebarNav"] ul,
[data-testid="stSidebarNav"] li {
    background: transparent !important;
}

[data-testid="stSidebarNav"] a {
    background: transparent !important;
    color: white !important;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(0, 212, 255, 0.2) !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: #0077ff !important;
    color: white !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050816, #101b35, #172b4d) !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] * {
    background-color: transparent !important;
    color: white !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #0077ff !important;
}
/* Movie Card Border and Glow */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 15px;
    transition: all 0.3s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border: 1px solid #00d4ff !important;
    box-shadow: 0 0 25px #00d4ff !important;
    transform: translateY(-5px);
}

/* CINE AI Movie Card */
div[class*="st-key-movie-card-"] {
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 15px;
    transition: all 0.3s ease;
}

/* CINE AI Smooth Neon Hover */

div[class*="st-key-movie-card-"] {
    transition: box-shadow 0.3s ease, border-color 0.3s ease !important;
}

div[class*="st-key-movie-card-"]:hover {
    border: 1px solid #00d4ff !important;
    box-shadow:
        0 0 10px #00d4ff,
        0 0 25px rgba(0, 212, 255, 0.7),
        0 0 40px rgba(0, 212, 255, 0.4) !important;
    transform: none !important;
}
/* CINE AI Smooth Poster Zoom */

div[class*="st-key-movie-card-"] img {
    transition: transform 0.3s ease !important;
    border-radius: 12px;
    transform-origin: center;
}



div[class*="st-key-movie-card-"] img {
    width: 100% !important;
    height: auto !important;
    object-fit: contain !important;
    
}
div[class*="st-key-movie-card-"] img {
    transition: none !important;
    animation: none !important;
}
}
/* CINE AI Glassmorphism Cards */
div[class*="st-key-movie-card-"] {
    background: rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 18px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
/* CINE AI Glass Search Box */
div[data-testid="stTextInput"] input {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    color: white !important;
}

div[data-testid="stTextInput"] input:focus {
    border: 1px solid #00d4ff !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
}
/* CINE AI Glass Sidebar */
[data-testid="stSidebar"] {
    background: rgba(5, 8, 22, 0.85) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.15);
}

[data-testid="stSidebarNav"] a {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    margin-bottom: 8px;
}
/* CINE AI Mobile Responsive Design */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.7rem !important;
    }

    h1 {
        font-size: 26px !important;
    }

    h2 {
        font-size: 22px !important;
    }

    div[class*="st-key-movie-card-"] {
        border-radius: 12px !important;
    }

    [data-testid="stImage"] img {
        max-width: 100%;
        height: auto;
    }
}
/* CINE AI Mobile - 2 Cards Per Row */

@media screen and (max-width: 768px) {
    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-movie-card-"]) {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 12px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-movie-card-"]) > div[data-testid="column"] {
        flex: 0 0 calc(50% - 6px) !important;
        width: calc(50% - 6px) !important;
        min-width: 0 !important;
    }
}
}
/* CINE AI Mobile Glass Cards */
@media (max-width: 768px) {
    div[class*="st-key-movie-card-"],
    div[class*="st-key-movie-card-"] [data-testid="stVerticalBlockBorderWrapper"] {
       background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 212, 255, 0.5) !important;
        border-radius: 18px !important;
    }

}
/* CINE AI Glassmorphism Effect */

div[class*="st-key-movie-card-"],
div[class*="st-key-movie-card-"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
/* CINE AI Movie Card - Glass + Neon */

div[class*="st-key-movie-card-"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(0, 212, 255, 0.45) !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
    transition: box-shadow 0.3s ease, border-color 0.3s ease !important;
}

div[class*="st-key-movie-card-"]:hover [data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #00d4ff !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.6) !important;
}
/* CINE AI - Glass Card + Neon Glow */

div[class*="st-key-movie-card-"],
div[class*="st-key-movie-card-"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(0, 212, 255, 0.35) !important;
    border-radius: 18px !important;
    transition: box-shadow 0.3s ease, border-color 0.3s ease !important;
}

div[class*="st-key-movie-card-"]:hover,
div[class*="st-key-movie-card-"]:hover [data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #00d4ff !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.7) !important;
}
/* CINE AI - Final Movie Card Glass Effect */

div[data-testid="stVerticalBlockBorderWrapper"]:has(div[class*="st-key-movie-card-"]) {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(0, 212, 255, 0.5) !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
    transition: box-shadow 0.3s ease, border-color 0.3s ease !important;
    transform: none !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(div[class*="st-key-movie-card-"]):hover {
    border-color: #00d4ff !important;
    box-shadow: 0 0 10px #00d4ff,
                0 0 25px rgba(0, 212, 255, 0.7) !important;
}
/* CINE AI Search Text Fix */

div[data-testid="stTextInput"] input {
    background: #172b4d !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #00d4ff !important;
    border: 1px solid #00d4ff !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #bbbbbb !important;
    -webkit-text-fill-color: #bbbbbb !important;
}
/* CINE AI - Netflix Mobile Layout */
@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"]:has([class*="st-key-movie-card-"]) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        gap: 12px !important;
    }

    div[data-testid="stHorizontalBlock"]:has([class*="st-key-movie-card-"]) > div[data-testid="column"] {
        flex: 0 0 42% !important;
        width: 42% !important;
        min-width: 42% !important;
        max-width: 42% !important;
    }
}
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


# CINE AI - Professional Homepage

st.html("""
<style>
.hero-section {
    text-align: center;
    padding: 55px 20px;
    margin: 15px 0 25px 0;
    border-radius: 24px;
    background: linear-gradient(135deg, #101b35, #050816);
    border: 1px solid rgba(0, 212, 255, 0.5);
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.12);
}

.hero-badge {
    display: inline-block;
    padding: 7px 16px;
    border-radius: 30px;
    background: rgba(0, 212, 255, 0.12);
    color: #00d4ff;
    font-size: 13px;
    font-weight: bold;
    border: 1px solid #00d4ff;
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    color: #00d4ff;
    margin: 22px 0 12px 0;
}

.hero-description {
    color: #cbd5e1;
    font-size: 17px;
    line-height: 1.7;
}

.hero-features {
    color: white;
    font-size: 14px;
    margin-top: 25px;
}

@media (max-width: 768px) {
    .hero-section {
        padding: 35px 12px;
    }

    .hero-title {
        font-size: 32px;
    }

    .hero-description {
        font-size: 14px;
    }
}
</style>

<div class="hero-section" id="home">

    <div class="hero-badge">
        ✨ AI POWERED MOVIE PLATFORM
    </div>

    <div class="hero-title">
        🎬 CINE AI
    </div>

    <div class="hero-description">
        Discover Movies You'll Love ❤️<br>
        Explore amazing movies and find your next favourite.
    </div>

    <div class="hero-features">
        🎥 Discover &nbsp; | &nbsp;
        🤖 AI Recommendations &nbsp; | &nbsp;
        ⭐ Top Rated Movies
    </div>
</div>
""")
# CINE AI Navigation Menu

st.html("""
<style>
.cine-nav {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 12px;
    padding: 15px;
    margin: 15px 0 25px 0;
    background: #101b35;
    border: 1px solid rgba(0,212,255,0.4);
    border-radius: 15px;
}

.cine-nav a {
    color: white;
    text-decoration: none;
    padding: 10px 18px;
    border-radius: 9px;
    font-size: 14px;
    font-weight: 600;
}

.cine-nav a:hover {
    background: #00d4ff;
    color: #050816;
}
</style>

<div class="cine-nav">
    <a href="#home">🏠 Home</a>
    <a href="#trending">🔥 Trending</a>
    <a href="#latest">🎬 Latest Movies</a>
    <a href="#movies-hub">🍿 Movies Hub</a>
</div>
""")


st.divider()

# Surprise Me Feature
st.markdown("### 🎲 Can't decide what to watch?")

if "surprise_movie" not in st.session_state:
    st.session_state.surprise_movie = None

button_text = (
    "🎲 Next Surprise 🔄"
    if st.session_state.surprise_movie
    else "🎲 Surprise Me"
)

if st.button(button_text, use_container_width=True):

    available_movies = movies

    if st.session_state.surprise_movie and len(movies) > 1:
        available_movies = movies[
            movies["title"] != st.session_state.surprise_movie
        ]

    st.session_state.surprise_movie = (
        available_movies.sample(1).iloc[0]["title"]
    )

if st.session_state.surprise_movie:

    random_movie = movies[
        movies["title"] == st.session_state.surprise_movie
    ].iloc[0]

    poster_url = get_movie_poster(random_movie["title"])

    movie_title = html.escape(str(random_movie["title"]))
    movie_genre = html.escape(str(random_movie["genre"]))
    movie_description = html.escape(str(random_movie["description"]))
    movie_rating = html.escape(str(random_movie["rating"]))

    poster_html = (
        f'<img src="{html.escape(poster_url, quote=True)}" class="surprise-poster">'
        if poster_url
        else '<div class="poster-placeholder">🎬 Poster Unavailable</div>'
    )

    st.html(textwrap.dedent(f"""
        <style>
        .surprise-card {{
            display: flex;
            gap: 22px;
            padding: 20px;
            margin-top: 15px;
            border-radius: 18px;
            background: linear-gradient(135deg, #101b35, #050816);
            border: 1px solid rgba(0, 212, 255, 0.65);
            box-shadow: 0 0 18px rgba(0, 212, 255, 0.18);
            transition: 0.3s ease;
        }}

        .surprise-card:hover {{
            border-color: #00d4ff;
            box-shadow: 0 0 28px rgba(0, 212, 255, 0.35);
            transform: translateY(-3px);
        }}

        .surprise-poster {{
            width: 180px;
            height: 270px;
            object-fit: cover;
            border-radius: 12px;
        }}

        .poster-placeholder {{
            width: 180px;
            height: 270px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #172b4d;
            border-radius: 12px;
            color: white;
        }}

        .surprise-details {{
            flex: 1;
            min-width: 0;
            color: white;
        }}

        .surprise-title {{
            color: #00d4ff;
            font-size: 25px;
            font-weight: 800;
            margin-bottom: 15px;
        }}

        .surprise-info {{
            font-size: 15px;
            margin-bottom: 12px;
            color: #dbeafe;
        }}

        .surprise-story {{
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.7;
            margin-top: 15px;
        }}

        @media (max-width: 600px) {{
            .surprise-card {{
                flex-direction: column;
                align-items: center;
                text-align: center;
            }}

            .surprise-poster,
            .poster-placeholder {{
                width: 160px;
                height: 240px;
            }}

            .surprise-title {{
                font-size: 21px;
            }}
        }}
        </style>

        <div class="surprise-card">
            <div>
                {poster_html}
            </div>

            <div class="surprise-details">
                <div class="surprise-title">
                    🎬 {movie_title}
                </div>

                <div class="surprise-info">
                    ⭐ Rating: {movie_rating}/5
                </div>

                <div class="surprise-info">
                    🎭 Genre: {movie_genre}
                </div>

                <div class="surprise-story">
                    <b>📖 Movie Story</b><br><br>
                    {movie_description}
                </div>
            </div>
        </div>
    """))

st.divider()


# Search Movie

# Top Rated Movies
# LATEST MOVIES SECTION
st.subheader("🎬 Latest Movies", anchor="latest")

latest_movies_data = []

with st.spinner("Loading latest movies..."):
    for _, row in movies.iterrows():
        title = row["title"]
        details = get_movie_details(title)

        if details and details.get("year"):
            year_text = str(details["year"])
            try:
                year = int(year_text[:4])
                latest_movies_data.append((title, year))
            except ValueError:
                pass
            

# Newest movies first
latest_movies_data.sort(key=lambda x: x[1], reverse=True)

if latest_movies_data:
    latest_five = latest_movies_data[:5]
    cols = st.columns(5)

    for col, (title, year) in zip(cols, latest_five):
        with col:
            poster = get_movie_poster(title)

            if poster:
                st.image(poster, use_container_width=True)

            st.markdown(f"**{title}**")
            st.caption(f"📅 {year}")
else:
    st.info("Latest movie information is not available.")
    # MOVIES HUB SECTION
st.subheader("🍿 Movies Hub", anchor="movies-hub")

st.write("Explore movies by your favourite genre.")

all_genres = sorted(set(
    genre.strip()
    for value in movies["genre"].dropna()
    for genre in str(value).replace("|", ",").split(",")
    if genre.strip()
))

selected_hub_genre = st.selectbox(
    "🎭 Choose Your Genre",
    all_genres,
    key="hub_genre"
)

hub_movies = movies[
    movies["genre"].str.contains(
        selected_hub_genre,
        case=False,
        na=False,
        regex=False
    )
].head(10)

if not hub_movies.empty:
    cols = st.columns(5)

    for index, (_, movie) in enumerate(hub_movies.iterrows()):
        with cols[index % 5]:
            poster = get_movie_poster(movie["title"])

            if poster:
                st.image(poster, use_container_width=True)

            st.markdown(f"**{movie['title']}**")
            st.caption(f"⭐ {movie['rating']}/5")
else:
    st.info("No movies found in this genre.")
# Top Rated Movies - Netflix Style
st.markdown('<div id="trending"></div>', unsafe_allow_html=True)
st.subheader("⭐ Top Rated Movies", anchor="trending")

top_movies = movies.sort_values(
    by="rating",
    ascending=False
).head(5)

movie_cards = ""

for _, movie in top_movies.iterrows():

    poster = get_movie_poster(movie["title"])

    title = html.escape(str(movie["title"]))
    genre = html.escape(str(movie["genre"]))
    rating = movie["rating"]

    if poster:
        poster_html = f'<img src="{html.escape(poster, quote=True)}">'
    else:
        poster_html = '<div class="no-poster">🎬 Poster unavailable</div>'

    movie_cards += f"""
    <div class="netflix-card">
        {poster_html}
        <h4>{title}</h4>
        <div class="movie-rating">⭐ {rating}/5</div>
        <p>{genre}</p>
    </div>
    """

st.markdown("""
<style>
.netflix-row {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 12px;
    width: 100%;
}

.netflix-card {
    min-width: 0;
    padding: 8px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(0,212,255,0.4);
    border-radius: 15px;
    text-align: center;
    transition: 0.3s ease;
}

.netflix-card:hover {
    border-color: #00d4ff;
    box-shadow: 0 0 18px rgba(0,212,255,0.6);
}

.netflix-card img {
    width: 100%;
    aspect-ratio: 2 / 3;
    object-fit: cover;
    border-radius: 10px;
}

.netflix-card h4 {
    color: white;
    font-size: 14px;
    margin: 10px 0;
}

.movie-rating {
    display: inline-block;
    background: linear-gradient(90deg, #ff9800, #ffcc00);
    color: black;
    padding: 4px 9px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 12px;
}

.netflix-card p {
    color: #bbbbbb;
    font-size: 11px;
}

.no-poster {
    aspect-ratio: 2 / 3;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

/* CINE AI - Mobile Netflix Grid */

@media screen and (max-width: 768px) {

    .netflix-row {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 12px !important;
        width: 100% !important;
        padding: 8px 0 !important;
    }

    .netflix-card {
        width: 100% !important;
        min-width: 0 !important;
        padding: 6px !important;
        border-radius: 12px !important;
    }

    .netflix-card img {
        width: 100% !important;
        height: 145px !important;
        object-fit: contain !important;
        background: #101b35 !important;
        border-radius: 10px !important;
    }

    .netflix-card h4 {
        font-size: 13px !important;
        line-height: 1.4 !important;
    }

    .netflix-card p {
        font-size: 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="netflix-row">{textwrap.dedent(movie_cards)}</div>',
    unsafe_allow_html=True
)
st.markdown("""
<style>

/* CINE AI - Final Mobile Poster Fix */

@media screen and (max-width: 768px) {

    .netflix-row {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 10px !important;
    }

    .netflix-row .netflix-card img {
        width: 100% !important;
        height: 140px !important;
        max-height: 140px !important;
        aspect-ratio: auto !important;
        object-fit: contain !important;
        display: block !important;
    }

    .netflix-row .netflix-card {
        min-width: 0 !important;
        padding: 5px !important;
    }
}

</style>
""", unsafe_allow_html=True)
# Search Movie
search_text = st.text_input(
    "🔍 Search Movie",
    placeholder="Type movie name here..."
)

filtered_movies = movies.copy()

   # Genre Filter
st.subheader("🎭 Choose Genre")

genres = ["All Genres"] + sorted(
    movies["genre"].dropna().unique().tolist()
)

selected_genre = st.selectbox(
    "Choose Genre",
    genres
)
if selected_genre != "All Genres":
    filtered_movies = filtered_movies[
        filtered_movies["genre"] == selected_genre
    ]

if search_text.strip():
    filtered_movies = filtered_movies[
        filtered_movies["title"].str.contains(
            search_text.strip(),
            case=False,
            na=False
        )
    ]

matching_movies = filtered_movies["title"].tolist()
st.markdown(
    f"""
    <div style="
        background: linear-gradient(90deg, #0077ff, #00d4ff);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        margin: 15px 0;
    ">
        🎬 {len(filtered_movies)} Movies Found
    </div>
    """,
    unsafe_allow_html=True
)

# Search Results
if matching_movies:
    st.success(f"🎬 Found {len(matching_movies)} movies!")

    if search_text.strip():
        st.subheader("🔎 Search Results")

        for _, movie in filtered_movies.head(5).iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([1, 2])

                poster = get_movie_poster(movie["title"])

                with col1:
                    if poster:
                        st.image(poster, width="stretch")
                    else:
                        st.write("🎬 Poster unavailable")

                with col2:
                    st.markdown(f"### 🎬 {movie['title']}")
                    st.write(f"⭐ Rating: {movie['rating']}/5")
                    st.write(f"🎭 Genre: {movie['genre']}")

        if len(matching_movies) > 5:
            st.info("Showing first 5 results. Select your movie below.")

else:
    st.warning("No movie found. Try another name.")

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

# Fetch OMDb Details
extra_details = get_movie_details(selected_movie)

st.divider()
st.subheader("🎥 Complete Movie Details")

with st.container(border=True):

    col1, col2 = st.columns([1, 2])

    poster_url = get_movie_poster(selected_movie)

    with col1:
        if poster_url:
            st.image(poster_url, width="stretch")
        else:
            st.info("🎬 Poster not available.")

    with col2:
        st.markdown(f"## 🎬 {movie_info['title']}")

        st.markdown(
            f"⭐ **Cine AI Rating:** {movie_info['rating']}/5"
        )

        st.markdown(
            f"🎭 **Genre:** {movie_info['genre']}"
        )

        if extra_details:

            st.markdown(
                f"⭐ **IMDb Rating:** {extra_details['imdb_rating']}/10"
            )

            st.markdown(
                f"📅 **Release Year:** {extra_details['year']}"
            )

            st.markdown(
                f"🎬 **Director:** {extra_details['director']}"
            )

            st.markdown(
                f"👥 **Actors:** {extra_details['actors']}"
            )

            st.markdown(
                f"⏱️ **Runtime:** {extra_details['runtime']}"
            )

            st.markdown(
                f"🌐 **Language:** {extra_details['language']}"
            )

        else:
            st.warning("Additional movie details are unavailable.")

        st.markdown("### 📖 Movie Story")

        if extra_details and extra_details["plot"] != "N/A":
            st.write(extra_details["plot"])
        else:
            st.write(movie_info["description"])

        st.link_button(
            "▶ Watch Movie Trailer",
            f"https://www.youtube.com/results?search_query={selected_movie.replace(' ', '+')}+official+trailer",
            use_container_width=True
        )
        # Watchlist Feature

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if st.button("❤️ Add to Watchlist"):

    if selected_movie not in st.session_state.watchlist:
        st.session_state.watchlist.append(selected_movie)
        st.success("Movie added to your Watchlist! ❤️")
    else:
        st.info("Movie is already in your Watchlist.")

st.divider()
# My Watchlist
st.markdown("<div id='my-watchlist'></div>", unsafe_allow_html=True)
st.subheader("❤️ My Watchlist")

def remove_from_watchlist(movie):
    st.session_state.watchlist.remove(movie)

if st.session_state.watchlist:

    for movie in st.session_state.watchlist:

        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"🎬 {movie}")

        with col2:
            st.button(
                "❌ Remove",
                key=f"remove_{movie}",
                on_click=remove_from_watchlist,
                args=(movie,)
            )

else:
    st.info("Your Watchlist is empty!")
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
                st.image(poster, width="stretch")
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
# CINE AI - Global Poster Size Fix

st.markdown("""
<style>

/* Top Rated Movie Posters */

.netflix-row .netflix-card img {
    width: 100% !important;
    height: 170px !important;
    object-fit: contain !important;
}

/* Search, Details and Recommendation Posters */

[data-testid="stImage"] img {
    width: 100% !important;
    height: 180px !important;
    max-height: 180px !important;
    object-fit: contain !important;
    border-radius: 10px !important;
}

/* Mobile Poster Design */

@media screen and (max-width: 768px) {

    .netflix-row {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 10px !important;
    }

    .netflix-row .netflix-card img {
        height: 145px !important;
    }

    [data-testid="stImage"] img {
        height: 160px !important;
        max-height: 160px !important;
    }
}
/* Cine AI Trailer Button */

div[data-testid="stLinkButton"] a {
    background: linear-gradient(135deg, #00d4ff, #0066ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stLinkButton"] a:hover {
    background: linear-gradient(135deg, #0066ff, #00d4ff) !important;
    box-shadow: 0 0 18px rgba(0, 212, 255, 0.6) !important;
    transform: scale(1.03);
}
/* Mobile Trailer Button Fix */

@media (max-width: 768px) {
    div[data-testid="stLinkButton"] a {
        background: linear-gradient(135deg, #00d4ff, #0066ff) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4) !important;
    }

    div[data-testid="stLinkButton"] a p {
        color: #ffffff !important;
    }
}
</style>
""", unsafe_allow_html=True)