"""REST API for movie-recommender.html (same logic as Streamlit)."""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import recommender_core as rc

DIR = Path(__file__).resolve().parent

app = FastAPI(title="CineMatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    rc.ensure_data()


class RecommendBody(BaseModel):
    title: str


@app.get("/api/movies")
def get_movies():
    return rc.movies_catalog()


@app.post("/api/recommend")
def recommend_api(body: RecommendBody):
    try:
        names, posters, ids = rc.recommend(body.title)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return {
        "recommendations": [
            {"title": names[i], "movie_id": ids[i], "poster_url": posters[i]}
            for i in range(len(names))
        ]
    }


@app.get("/poster/{movie_id}")
def poster_meta(movie_id: int):
    """TMDB poster path JSON for the HTML fallback fetcher."""
    try:
        url = rc.fetch_poster(movie_id)
        if "placeholder" in url.lower():
            return {"poster_path": None}
        # Return a path fragment the HTML can turn into full URL, or full URL
        if url.startswith("https://image.tmdb.org"):
            path = url.replace("https://image.tmdb.org/t/p/w500", "")
            return {"poster_path": path}
        return {"poster_path": None}
    except Exception:
        return {"poster_path": None}


@app.get("/")
def serve_ui():
    return FileResponse(DIR / "movie-recommender.html")
