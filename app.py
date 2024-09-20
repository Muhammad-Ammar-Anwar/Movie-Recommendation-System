import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('api_key')

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    
    
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return 'https://via.placeholder.com/500x750?text=No+Image'  # Return a placeholder if no poster is found

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]  # Get top 10 recommendations

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))  # fetching posters from API
    return recommended_movies, recommended_movie_posters



movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


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




