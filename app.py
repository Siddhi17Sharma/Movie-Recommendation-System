import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

# --------------------- SETUP ---------------------
load_dotenv()
st.set_page_config(page_title="Movie Recommender", layout="wide")
API_KEY = os.getenv("TMDB_API_KEY")

# Load movie data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --------------------- UTILITY FUNCTIONS ---------------------
def fetch_movie_data(title, language_code="en"):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language={language_code}&query={quote(title)}"
        response = requests.get(url)
        data = response.json()
        if data['results']:
            movie = data['results'][0]
            poster_path = movie.get('poster_path')
            release_date = movie.get('release_date', '')
            vote_average = movie.get('vote_average', 'N/A')
            overview = movie.get('overview', 'No overview available.')
            trailer_url = get_trailer_url(movie['id'])
            return {
                'poster': f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Image",
                'release_year': release_date[:4] if release_date else 'N/A',
                'rating': vote_average,
                'overview': overview,
                'trailer_url': trailer_url
            }
        return None
    except Exception as e:
        print(f"Error fetching movie data: {e}")
        return None

def get_trailer_url(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
        response = requests.get(url)
        videos = response.json().get('results', [])
        for video in videos:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                return f"https://www.youtube.com/watch?v={video['key']}"
        return None
    except:
        return None

def recommend(movie, language_code="en", genre_filter=None):
    movie = movie.lower()
    filtered_df = movies

    if genre_filter:
        filtered_df = filtered_df[filtered_df['tags'].str.contains(genre_filter, case=False, na=False)]

    matched_movies = filtered_df[filtered_df['title'].str.lower() == movie]
    if matched_movies.empty:
        return []

    index = matched_movies.index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommendations = []
    for i in distances[1:11]:
        title = movies.iloc[i[0]].title
        movie_info = fetch_movie_data(title, language_code)
        if movie_info:
            movie_info['title'] = title
            recommendations.append(movie_info)
    return recommendations

# --------------------- STREAMLIT UI ---------------------
st.title("Movie Recommender System")
st.markdown("Enter a movie name to get similar recommendations.")

languages = {
    "English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr",
    "German": "de", "Japanese": "ja", "Korean": "ko", "Italian": "it",
    "Chinese": "zh", "Portuguese": "pt"
}
genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Horror', 'Romance', 'Thriller']

col1, col2 = st.columns(2)
with col1:
    lang_choice = st.selectbox("Select Language", list(languages.keys()))
with col2:
    genre_choice = st.selectbox("Optional Genre Filter", ["None"] + genres)

user_input = st.text_input("Movie Title", "The Avengers")

# Suggestion if movie not found
suggested_titles = [t for t in movies['title'].values if user_input.lower() in t.lower()][:3]
if user_input and not any(user_input.lower() == t.lower() for t in movies['title'].values):
    if suggested_titles:
        st.markdown("**Did you mean:**")
        for title in suggested_titles:
            if st.button(title, key=f"suggestion_{title}"):
                user_input = title

if st.button("Recommend", key="recommend_button"):
    with st.spinner("Fetching recommendations..."):
        language_code = languages[lang_choice]
        genre_filter = None if genre_choice == "None" else genre_choice
        results = recommend(user_input, language_code, genre_filter)

    if results:
        st.subheader("Recommended Movies")
        for row in range(0, len(results), 5):
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                if row + idx < len(results):
                    movie = results[row + idx]
                    with col:
                        st.image(movie['poster'], caption=movie['title'], use_container_width=True)
                        st.markdown(f"**Year:** {movie['release_year']}")
                        st.markdown(f"**Rating:** {movie['rating']}")
                        with st.expander("Overview"):
                            st.write(movie['overview'])
                        if movie['trailer_url']:
                            st.markdown(f"[Watch Trailer](https://www.youtube.com/watch?v={movie['trailer_url'][-11:]})", unsafe_allow_html=True)
    else:
        st.error("No matching recommendations found.")