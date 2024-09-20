import pandas as pd
import numpy as np

credits=pd.read_csv(r"C:\Users\Ammar\Documents\Project\tmdb_5000_credits.csv")
credits.head(1)

movies=pd.read_csv(r'C:\Users\Ammar\Documents\Project\tmdb_5000_movies.csv')
movies.head(1)

movies=movies.merge(credits,on='title')

''' List Of Important Features
genres
id
keywords
title
overview
cast
crew
'''
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.info()

movies.dropna(inplace=True)

import ast
def convert(obj):
  l=[]
  for i in ast.literal_eval(obj):

      l.append(i['name'])
  return l


movies.info()

movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)

movies['genres']

movies.head()
movies['cast'].values

def convert3(obj):
  l=[]
  counter=0
  for i in ast.literal_eval(obj):
    if counter != 3:
      l.append(i['name'])
      counter += 1
    else:
      break
  return l


movies['cast']=movies['cast'].apply(convert3)

movies['crew'][0]

def fetch_director(obj):
  l=[]
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      l.append(i['name'])
      break
  return l

movies['crew']=movies['crew'].apply(fetch_director)

movies.head()

movies['overview'][0]

movies['overview']=movies['overview'].apply(lambda x:x.split())

movies.head()

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])

movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])

movies

movies['tags']=movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.head()

new_df=movies[['movie_id','title','tags']]

new_df

new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))

new_df['tags'][0]

new_df['tags']=new_df['tags'].apply(lambda x: x.lower())

new_df.head()

new_df['tags'][0]

import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))

  return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')

vectors=cv.fit_transform(new_df['tags']).toarray()

vectors[0]

cv.get_feature_names_out()

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vectors)

def recommend(movie):
  movie_index=new_df[new_df['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  for i in movies_list:
    print(new_df.iloc[i[0]].title)


recommend('Batman Begins')

new_df[new_df['title']=='Batman Begins'].index[0]

sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]

import pickle
pickle.dump(new_df.to_dict(),open('movies_dict.pkl','wb'))

pickle.dump(similarity,open('similarity.pkl','wb'))
