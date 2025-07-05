# 🎬 Movie Recommender System

A content-based movie recommendation web app that suggests similar movies based on your input using **cosine similarity** on movie metadata. Built with **Python, Streamlit**, and integrated with the **TMDb API** for posters, ratings, overviews, and trailers.

---

## 🚀 Features

- 🔍 **Search by Title:** Enter any movie name to get similar movie recommendations.
- 📸 **Movie Posters:** Dynamically fetch and display posters via TMDb.
- 🗓️ **Year & Ratings:** Each recommended movie shows release year and rating (e.g., ⭐ 7.2/10).
- 📃 **Overview on Click:** Expand to view a brief overview.
- 🎞️ **Watch Trailer:** Open YouTube trailer with one click.
- 🌐 **Language Filter:** Choose from 10+ languages (e.g., English, Hindi, Spanish, etc.).
- 🎭 **Genre Filter:** Filter recommendations by genre (e.g., Action, Comedy, Drama).
- ✅ **Real-time Suggestions:** Auto-suggest movies as you type with typo correction.
- ⚙️ **Robust Backend:** Uses TMDb’s `/search`, `/movie/{id}`, and `/videos` endpoints.

---

## 🧠 Tech Stack

| Component      | Technology               |
|----------------|--------------------------|
| Backend Logic  | Python, Pandas, Scikit-learn |
| Web Framework  | Streamlit                |
| Recommendation | Cosine Similarity (CountVectorizer) |
| Movie Metadata | TMDb API (The Movie Database) |
| UI Features    | Streamlit widgets, columns, expanders |

---

## 📁 Dataset

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

These files are preprocessed and merged to extract metadata including:
- Title
- Overview
- Genre
- Cast
- Director
- Keywords

---

## 🔑 TMDb API Key

To fetch real-time data like posters, ratings, and trailers, you must have a TMDb API key.

1. Sign up at [https://www.themoviedb.org/](https://www.themoviedb.org/)
2. Navigate to **Settings > API** and generate your key
3. Replace the placeholder in `app.py`:
```python
API_KEY = "your_tmdb_api_key_here"
```

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## ✅ Sample Usage

1. Enter a movie name like `"The Avengers"`.
2. Choose language → English
3. Optionally filter genre → Action
4. Hit **"Recommend"**.
5. Browse posters, view overviews, and watch trailers.

---

## 🧹 To Do / Improvements

- Add login/signup with user-based watchlists
- Hybrid filtering (content + collaborative)
- IMDb/RottenTomatoes integration
- Pagination or infinite scroll

---

## 📄 License

MIT License © 2025 [Your Name]