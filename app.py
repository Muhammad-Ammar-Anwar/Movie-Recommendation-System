import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown  
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('api_key')

if not api_key:
    st.error("API key not found! Please set it in the .env file.")
    st.stop()


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return 'https://via.placeholder.com/500x750?text=No+Image'  


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]  # Get top 10 recommendations

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))  # Fetching posters from API
    return recommended_movies, recommended_movie_posters


drive_file_url = 'https://drive.google.com/uc?id=1Qrhtw4vmaoa9OltKoqyvJUbYBO7wCBUc'

if not os.path.exists('similarity.pkl'):
    try:
        st.write("Downloading similarity.pkl from Google Drive...")
        gdown.download(drive_file_url, 'similarity.pkl', quiet=False)
    except Exception as e:
        st.error(f"Error downloading the similarity.pkl file: {e}")
        st.stop()


try:
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("similarity.pkl file not found, please check if it was downloaded correctly.")
    st.stop()
except pickle.UnpicklingError:
    st.error("Error loading the similarity.pkl file. It might be corrupted.")
    st.stop()


try:
    with open('movies_dict.pkl', 'rb') as f:
        movie_dict = pickle.load(f)
    movies = pd.DataFrame(movie_dict)
except FileNotFoundError:
    st.error("movies_dict.pkl file not found, please check the file path.")
    st.stop()
except pickle.UnpicklingError:
    st.error("Error loading the movies_dict.pkl file. It might be corrupted.")
    st.stop()


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to conduct the search?',
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    
    cols1 = st.columns(5)
    cols2 = st.columns(5)
    
    for idx, col in enumerate(cols1):
        with col:
            st.markdown(f"<h3 style='font-size:14px; font-family:Courier; text-align:center;'>{names[idx]}</h3>", unsafe_allow_html=True)
            st.image(posters[idx], use_column_width=True)
    
    for idx, col in enumerate(cols2):
        with col:
            st.markdown(f"<h3 style='font-size:14px; font-family:Courier; text-align:center;'>{names[idx+5]}</h3>", unsafe_allow_html=True)
            st.image(posters[idx+5], use_column_width=True)




