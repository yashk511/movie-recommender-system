import streamlit as st
import pickle
from recommend import recommend

# Load movie titles
movies = pickle.load(open('movies.pkl', 'rb'))

st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Choose a movie:", movies['title'].values)

if st.button("Recommend"):
    with st.spinner("Fetching recommendations..."):
        recommendations = recommend(selected_movie)

    for title, poster, rating, overview in recommendations:
        st.markdown(f"### 🎥 {title}")
        cols = st.columns([1, 2])
        with cols[0]:
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.markdown("No poster available.")
        with cols[1]:
            st.markdown(f"**⭐ IMDb Rating:** {rating}")
            st.markdown(f"**📝 Overview:** {overview}")
        st.markdown("---")
