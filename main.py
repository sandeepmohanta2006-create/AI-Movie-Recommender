import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("===================================")
print("AI MOVIE RECOMMENDATION SYSTEM")
print("===================================")

movies = pd.read_csv("movies.csv")

movies["features"] = (
movies["genre"].fillna("") + " " +
movies["genre"].fillna("") + " " +
movies["description"].fillna("")
)

vectorizer = TfidfVectorizer(stop_words="english")
feature_matrix = vectorizer.fit_transform(movies["features"])

similarity = cosine_similarity(feature_matrix)

print("\nAvailable Movies:")

for i, title in enumerate(movies["title"], start=1):
    print(f"{i}. {title}")

movie_number = int(input("\nEnter a movie number: ")) - 1

if 0 <= movie_number < len(movies):
    scores = list(enumerate(similarity[movie_number]))
    scores.sort(key=lambda x: x[1], reverse=True)


print("\nMovies similar to", movies.iloc[movie_number]["title"])
print("\nRecommended Movies:")

count = 0

for index, score in scores:
    if index != movie_number:
        print("-", movies.iloc[index]["title"])
        count += 1

        if count == 5:
            break


else:
    print("Invalid movie number. Please select from the list.")
