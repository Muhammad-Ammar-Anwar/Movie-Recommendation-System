"""Shared movie data loading and recommendation logic for Streamlit and the API."""
import os
import pickle

import gdown
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")

movies = None
similarity = None

DRIVE_FILE_URL = "https://drive.google.com/uc?id=1Qrhtw4vmaoa9OltKoqyvJUbYBO7wCBUc"


def ensure_data():
    """Load pickles and similarity matrix once."""
    global movies, similarity
    if movies is not None and similarity is not None:
        return

    if not api_key:
        raise RuntimeError("API key not found. Set api_key in .env")

    if not os.path.exists("similarity.pkl"):
        gdown.download(DRIVE_FILE_URL, "similarity.pkl", quiet=False)

    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

    with open("movies_dict.pkl", "rb") as f:
        movie_dict = pickle.load(f)
    movies = pd.DataFrame(movie_dict)


def fetch_poster(movie_id: int) -> str:
    ensure_data()
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US",
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie_title: str):
    """Return (titles, poster_urls) for top 10 similar movies."""
    ensure_data()
    match = movies[movies["title"] == movie_title]
    if match.empty:
        raise ValueError(f"Movie not found: {movie_title!r}")
    movie_index = match.index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:11]

    recommended_movies = []
    recommended_posters = []
    recommended_ids = []
    for i in movies_list:
        movie_id = int(movies.iloc[i[0]].movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        recommended_ids.append(movie_id)
    return recommended_movies, recommended_posters, recommended_ids


def movies_catalog():
    """List of {title, movie_id} for the frontend."""
    ensure_data()
    return [
        {"title": str(row["title"]), "movie_id": int(row["movie_id"])}
        for _, row in movies.iterrows()
    ]
