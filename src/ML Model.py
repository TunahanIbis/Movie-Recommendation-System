import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Load JSON file
with open("movies.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert 'results' list into a DataFrame
movies_df = pd.DataFrame(data["results"])

# Genre ID mapping
genre_mapping = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}

# Function to convert genre IDs to genre names
def convert_genre_ids(genre_ids):
    if isinstance(genre_ids, list):
        return [genre_mapping.get(genre_id, "Unknown") for genre_id in genre_ids]
    return ["Unknown"]  # Handle cases where genre_ids is not a list

# Ensure that genre_ids column contains lists, not strings
movies_df["genre_ids"] = movies_df["genre_ids"].apply(convert_genre_ids)

movies_df["genres"] = movies_df["genre_ids"].apply(convert_genre_ids)

print(movies_df[["title", "genre_ids"]].head())

# --------- MACHINE LEARNING (ML) PROCESS ----------

# Vectorize the properties with TF-IDF
# 1. Convert genre ID's to a string for vectorization
movies_df["genres_str"] = movies_df["genre_ids"].apply(lambda x: ' '. join(map(str, x)))
genre_vectorizer = TfidfVectorizer()
genre_matrix = genre_vectorizer.fit_transform(movies_df["genres_str"])

# 2. Apply TF-IDF to movie overviews
overview_vectorizer = TfidfVectorizer(stop_words = 'english') # Used 'stop_words' to skip basic conjunctions, prepositions, and etc.
overview_matrix = overview_vectorizer.fit_transform(movies_df["overview"])

# 3. Extract the release year from the release date and apply TF-IDF
movies_df["release_year"] = movies_df["release_date"].apply(lambda x: x[:4])
year_encoder = OneHotEncoder(handle_unknown = "ignore", sparse_output = True)
year_matrix = year_encoder.fit_transform(movies_df[["release_year"]])

# Combine all the vectoral properties
movie_matrix = hstack([genre_matrix, overview_matrix, year_matrix])

print(movie_matrix.shape)

# Calculate the cosine similarity
cosine_sim = cosine_similarity(movie_matrix, movie_matrix)

# Check the cosine similarity
print(cosine_sim.shape)
print(cosine_sim[0])

# --------- RECOMMENDATION SYSTEM --------
def get_recommendation(movie_title, cosine_sim = cosine_sim, movies_df = movies_df):
    # Find the index of the film
    idx_movie = movies_df.index[movies_df['title'] == movie_title].tolist()[0]

    # Get the cosine similarity scores
    cos_sim_score = list(enumerate(cosine_sim[idx_movie]))

    # Sort the cosine similarity scores
    cos_sim_score = sorted(cos_sim_score, key = lambda x: x[1], reverse = True)

    # Get the 5 most similar movies (exclude the first one because that is the movie itself)
    cos_sim_score = cos_sim_score[1:6]

    # Take the indices of similar movies
    movie_indices = [i[0] for i in cos_sim_score]

    # Return the recommended movies
    return movies_df.iloc[movie_indices]

recommendation1 = get_recommendation(movies_df.iloc[23]['title'])
print(recommendation1[['title', 'genre_ids']])

# Save the vectorizers, OneHotEncoder, matrices and similarity matrix
# Save the TF-IDF vectorizers
joblib.dump(genre_vectorizer, 'genre_vectorizer.pkl')
joblib.dump(overview_vectorizer, 'overview_vectorizer.pkl')

# Save the OneHotEncoder for release years
joblib.dump(year_encoder, 'year_encoder.pkl')

# Save the computed matrices
joblib.dump(genre_matrix, 'genre_matrix.pkl')
joblib.dump(overview_matrix, 'overview_matrix.pkl')
joblib.dump(year_matrix, 'year_matrix.pkl')
joblib.dump(movie_matrix, 'movie_matrix.pkl')

# Save the cosine similarity matrix
joblib.dump(cosine_sim, 'cosine_sim_matrix.pkl')

# Save the DataFrame
movies_df.to_csv('movies_df.csv', index=False)

