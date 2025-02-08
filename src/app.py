import json
import os
import random
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Run the Flask app
app = Flask(__name__)

# ------------ LOAD THE MODELS -----------

# Define the path to the 'data/models' directory
models_dir = os.path.join(os.path.dirname(__file__), "..", "data", "models")

# Load vectorizers
genre_vectorizer = joblib.load(os.path.join(models_dir, "genre_vectorizer.pkl"))
overview_vectorizer = joblib.load(os.path.join(models_dir, "overview_vectorizer.pkl"))

# Load OneHotEncoder
year_encoder = joblib.load(os.path.join(models_dir, "year_encoder.pkl"))

# Load computed matrices
genre_matrix = joblib.load(os.path.join(models_dir, "genre_matrix.pkl"))
overview_matrix = joblib.load(os.path.join(models_dir, "overview_matrix.pkl"))
year_matrix = joblib.load(os.path.join(models_dir, "year_matrix.pkl"))
movie_matrix = joblib.load(os.path.join(models_dir, "movie_matrix.pkl"))

# Load cosine similarity matrix
cosine_sim = joblib.load(os.path.join(models_dir, "cosine_sim_matrix.pkl"))

# ----------- RECOMMENDATION MODEL -----------

# Define the path to the 'data/json' directory
json_dir = os.path.join(os.path.dirname(__file__), "..", "data", "json")

# Load JSON file
with open(os.path.join(json_dir, "movies.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert 'results' list into a DataFrame
movies_df = pd.DataFrame(data["results"])

# Genre ID mapping
genre_mapping = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western",
}


# Function to convert genre IDs to genre names
def convert_genre_ids(genre_ids):
    if isinstance(genre_ids, list):
        return [genre_mapping.get(genre_id, "Unknown") for genre_id in genre_ids]
    return ["Unknown"]  # Handle cases where genre_ids is not a list


# Ensure that genre_ids column contains lists, not strings
movies_df["genre_ids"] = movies_df["genre_ids"].apply(convert_genre_ids)

movies_df["genres"] = movies_df["genre_ids"].apply(convert_genre_ids)


def get_recommendations(selected_movies):
    try:
        # Find the indices of the selected movies
        indices = [
            movies_df.index[movies_df["title"] == title].tolist()[0]
            for title in selected_movies
        ]

        # Calculate the average similarity scores for each movie
        avg_sim = sum(cosine_sim[idx] for idx in indices) / len(indices)

        # Sort the movies based on similarity score
        sim_scores = list(enumerate(avg_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Select the top 3 most similar movies, excluding the selected ones
        recommended_indices = [i[0] for i in sim_scores if i[0] not in set(indices)][:3]

        # Return the recommended movies with their titles, genres, and posters
        return movies_df.iloc[recommended_indices][
            ["title", "genre_ids", "id", "poster_path"]
        ].to_dict(orient="records")
    except IndexError:
        return []  # Return an empty list if an IndexError occurs


# Initialize Flask app with correct template and static folders
app = Flask(__name__, template_folder="../templates", static_folder="../static")


# Example route to render the HTML page
@app.route("/")
def index():
    return render_template("index.html")


# Endpoint for random movie selection
@app.route("/random_movies", methods=["GET"])
def random_movies():
    # Select 10 random movies from the dataset (ensure movies_df is correctly loaded)
    random_movies = random.sample(movies_df.to_dict(orient="records"), 10)
    return jsonify(random_movies)


# Endpoint for movie recommendations
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    selected_movies = data.get("selected_movies", [])

    if len(selected_movies) != 3:
        return jsonify({"ERROR": "Please select exactly 3 movies."}), 400

    recommendations = get_recommendations(selected_movies)
    return jsonify({"recommendations": recommendations})


# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
