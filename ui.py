import streamlit as st
import pandas as pd
from src.recommender import get_movie_recommendations  # your existing recommender function

# Title of the app
st.title("🎬 Movie Recommender System")

st.write("""
Enter a movie you like, and get personalized recommendations!
""")

# Load data once
@st.cache_data
def load_data():
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    df = pd.merge(ratings, movies, on="movieId")
    return df

df = load_data()

# User input
movie_title = st.text_input("Enter a movie title:")

# Recommend button
if st.button("Get Recommendations"):
    if movie_title.strip() == "":
        st.warning("Please enter a movie name!")
    else:
        recommendations = get_movie_recommendations(df, movie_title)
        if len(recommendations) == 0:
            st.info("No recommendations found.")
        else:
            st.subheader(f"Movies recommended if you like '{movie_title}':")
            for i, movie in enumerate(recommendations, start=1):
                st.write(f"{i}. {movie}")
