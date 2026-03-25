from __future__ import annotations

from typing import Any, Dict

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import recommender_core as rc

app = Flask(__name__)
cors = CORS(app)

_loaded = False


def ensure_loaded() -> None:
    global _loaded
    if _loaded:
        return
    rc.ensure_data()
    _loaded = True


@app.get("/api/movies")
def api_movies():
    ensure_loaded()
    return jsonify(rc.movies_catalog())


@app.post("/api/recommend")
def api_recommend():
    ensure_loaded()
    payload: Dict[str, Any] | None = request.get_json(silent=True)
    if not payload or "title" not in payload:
        return jsonify({"detail": "Missing 'title'"}), 400

    try:
        names, posters, ids = rc.recommend(payload["title"])
    except ValueError as e:
        return jsonify({"detail": str(e)}), 404
    except Exception as e:
        return jsonify({"detail": f"Server error: {e}"}), 500

    return jsonify(
        {
            "recommendations": [
                {"title": names[i], "movie_id": ids[i], "poster_url": posters[i]}
                for i in range(len(names))
            ]
        }
    )


@app.get("/poster/<int:movie_id>")
def poster_meta(movie_id: int):
    """
    Optional endpoint. Your current HTML uses `poster_url` from /api/recommend,
    so this is mostly for backward compatibility.
    """
    try:
        poster_url = rc.fetch_poster(movie_id)
    except Exception:
        poster_url = None
    return jsonify({"poster_url": poster_url})


@app.get("/")
def ui():
    """Serve the frontend for local testing."""
    import os
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "movie-recommender_2.html",
    )


if __name__ == "__main__":
    # Local dev:
    #   python flask_app.py
    # then open http://127.0.0.1:5000/
    app.run(host="127.0.0.1", port=5000, debug=True)

