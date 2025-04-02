import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=634eb4c3cd58591a03bcda1d95d1b5ac&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    # Check if the movie exists in the DataFrame
    if movie not in movies['title'].values:
        return [], []  # Return empty lists if the movie is not found

    # Find the index of the movie
    index = movies[movies['title'] == movie].index[0]

    # Calculate similarity
    distance = similarity[index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    # Prepare recommendations
    reco_names = []
    reco_posters = []
    for i in movie_list:
        # Replace 'id' with the correct column name that contains movie IDs
        movie_id = movies.iloc[i[0]]['movie_id']  # Adjust 'movie_id' based on your DataFrame
        reco_names.append(movies.iloc[i[0]].title)
        reco_posters.append(fetch_poster(movie_id))
    return reco_names, reco_posters



movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
st.title('ReelReco')

Selected = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(Selected)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])







