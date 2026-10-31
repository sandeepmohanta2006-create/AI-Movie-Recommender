import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pathlib import Path

movies = pd.read_csv(
    Path(__file__).resolve().parent / "movies.csv",
    encoding="utf-8-sig"
)

print("CSV Columns:", repr(movies.columns.tolist()))
print("CSV File:", movies.head(2))

print("CSV Columns:", movies.columns.tolist())
print("CSV File:", movies.columns.tolist())
print("First rows:", movies.head(2).to_dict())

movies["features"] = (
    movies["genre"].fillna("") + " " +
    movies["description"].fillna("")
)

vectorizer = TfidfVectorizer(stop_words="english")
feature_matrix = vectorizer.fit_transform(movies["features"])
similarity = cosine_similarity(feature_matrix)

root = tk.Tk()

root.title("AI Movie Recommendation System")
root.geometry("900x750")
root.resizable(False, False)
root.configure(bg="#0F172A")
heading = tk.Label(
    root,
    text="AI MOVIE RECOMMENDER",
    font=("Arial", 24, "bold"),
    bg="#0F172A",
    fg="white"
)

heading.pack(pady=20)

subtitle = tk.Label(
    root,
    text="Discover your next favourite movie with AI!",
    font=("Arial", 12),
    bg="#172033",
    fg="#cbd5e1"
)
subtitle.pack(pady=5)
total_movies_label = tk.Label(
root,
text=f"🎬 Total Movies: {len(movies)}",
font=("Arial", 12, "bold"),
bg="#172033",
fg="#4ade80"
)
total_movies_label.pack(pady=8)


movie_label = tk.Label(
    root,
    text="Select a movie:",
    font=("Arial", 12, "bold"),
    bg="#172033",
    fg="white"
)
movie_label.pack(pady=(20, 5))

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground="#1E293B",
    background="#2563EB",
    foreground="white",
    arrowcolor="white"
)

movie_box = ttk.Combobox(
    root,
    values=movies["title"].tolist(),
    state="readonly",
    width=35,
    font=("Arial", 11)
)

movie_box.pack(pady=5)
movie_box.current(0)

search_label = tk.Label(
    root,
    text="Search Movie:",
    font=("Arial", 12, "bold"),
    bg="#0F172A",
    fg="white"
)

search_label.pack(pady=(15, 5))

search_box = tk.Entry(
    root,
    font=("Arial", 12),
    width=35,
    bg="#1E293B",
    fg="white",
    insertbackground="white",
    relief="flat"
)

search_box.pack(pady=5, ipady=7)
search_box.pack(pady=5)


def search_movie(event=None):
    search_text = search_box.get().lower().strip()

    matching_movies = [
        title for title in movies["title"].tolist()
        if search_text in title.lower()
    ]

    movie_box["values"] = matching_movies

    if matching_movies:
        movie_box.current(0)
    else:
        movie_box.set("")


search_box.bind("<KeyRelease>", search_movie)


def clear_search():
    search_box.delete(0, tk.END)
    movie_box["values"] = movies["title"].tolist()
    movie_box.set("")
    results.delete("1.0", tk.END)
    movie_details.config(
        text="Select a movie to see its details."
    )


clear_button = tk.Button(
    root,
    text="🧹 Clear Search",
    command=clear_search,
    font=("Arial", 11, "bold"),
    bg="#DC2626",
    fg="white",
    activebackground="#B91C1C",
    activeforeground="white",
    cursor="hand2",
    padx=20,
    pady=10,
    relief="flat",
    borderwidth=0
)

clear_button.pack(pady=8)



def recommend_movies():
    selected_movie = movie_box.get()

    if not selected_movie:
        messagebox.showwarning("Warning", "Please select a movie.")
        return

    movie_info = movies[movies["title"] == selected_movie].iloc[0]

    movie_details.config(
        text="Genre: " + str(movie_info["genre"]) +
        "\nRating: " + str(movie_info["rating"]) + "/5" +
        "\n\nDescription: " + str(movie_info["description"])
    )

    movie_index = movies.index[
        movies["title"] == selected_movie
    ][0]

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

    results.delete("1.0", tk.END)
    results.insert(tk.END, "Recommended Movies\n")
    results.insert(tk.END, "-" * 35 + "\n\n")
    count = 0

    for index, score in scores:
        if score < 0.25:
            continue

        results.insert(
            tk.END,
            "- " + movies.iloc[index]["title"] +
            " (Rating: " +
            str(movies.iloc[index]["rating"]) + "/5)\n"
        )

        count += 1

        if count == 5:
            break

    if count == 0:
        results.insert(tk.END, "No similar movies found.")
   

movie_details = tk.Label(
    root,
    text="Select a movie to see its details.",
    font=("Arial", 11),
    bg="#1E293B",
    fg="#E2E8F0",
    wraplength=650,
    justify="left",
    padx=20,
    pady=15
)

movie_details.pack(pady=10, fill="x", padx=25)

recommend_button = tk.Button(
    root,
    text="🎬 Recommend Movies",
    command=recommend_movies,
    font=("Arial", 12, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    cursor="hand2",
    padx=25,
    pady=12,
    relief="flat",
    borderwidth=0
)

recommend_button.pack(pady=15)

results = tk.Text(
    root,
    height=8,
    width=65,
    font=("Arial", 11),
    bg="#1E293B",
    fg="#E2E8F0",
    insertbackground="white",
    wrap="word",
    relief="flat",
    padx=15,
    pady=10
)

results.pack(pady=10, padx=25)

root.mainloop()