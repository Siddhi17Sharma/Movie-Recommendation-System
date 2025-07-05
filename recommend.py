import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import pickle

# TMDB API Key
API_KEY = "8fbf9fe625373bc7dc09794ef071d677"

# -------- Fetch Poster Function --------
def fetch_poster(title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=en-US&query={title}&include_adult=false"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['results'] and data['results'][0].get('poster_path'):
            poster_path = data['results'][0]['poster_path']
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            print(f"[!] No poster found for: {title}")
            return "https://via.placeholder.com/150?text=No+Image"
    except Exception as e:
        print(f"⚠️ Error fetching poster for '{title}': {e}")
        return "https://via.placeholder.com/150?text=Error"

# -------- Load and Merge Data --------
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')

# -------- Helper Functions --------
def convert(obj):
    try:
        return [i['name'] for i in ast.literal_eval(obj)]
    except:
        return []

def director(obj):
    try:
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                return i['name']
        return ''
    except:
        return ''

def collapse(lst):
    return [i.replace(" ", "") for i in lst]

# -------- Preprocess Features --------
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(lambda x: convert(x)[:3])
movies['crew'] = movies['crew'].apply(director)

movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(lambda x: x.replace(" ", ""))

movies['overview'] = movies['overview'].fillna('')
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# -------- Create Tags --------
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew'].apply(lambda x: [x])
new_df = movies[['movie_id', 'title', 'tags']].copy()
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# -------- Vectorize & Compute Similarity --------
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vectors)

# -------- Save to Pickle --------
pickle.dump(new_df, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

# -------- Recommendation Logic --------
def recommend(movie):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        print("❌ Movie not found.")
        return []

    index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    print(f"\nTop 5 recommendations for '{movie.title()}':\n")
    recommended = []
    for i in distances[1:6]:
        title = new_df.iloc[i[0]].title
        poster = fetch_poster(title)
        recommended.append((title, poster))
        print(f"🎬 {title}\n🖼️ Poster URL: {poster}\n")
    return recommended

# -------- CLI Mode for Testing --------
if __name__ == '__main__':
    while True:
        inp = input("\nEnter a movie name (or type 'exit' to quit): ")
        if inp.lower() == 'exit':
            break
        recommend(inp)