import streamlit as st

st.set_page_config(
    page_title="My Watchlist",
    page_icon="❤️",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #050816, #101b35, #172b4d);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

div.stButton > button {
    background: linear-gradient(90deg, #0077ff, #00d4ff);
    color: white !important;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}
/* Watchlist Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050816, #101b35, #172b4d) !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] a:hover {
    background-color: #0077ff !important;
}
</style>
""", unsafe_allow_html=True)

st.title("❤️ My Watchlist")
st.write("Your favourite movies in one place!")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []


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
    st.info("Your Watchlist is empty. Add your favourite movies!")