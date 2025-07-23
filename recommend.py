import pickle
import pandas as pd
import requests

with open('apikey.txt', 'r') as file:
    API_KEY = file.read().strip()

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_movie_id(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={requests.utils.quote(title)}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return data['results'][0]['id']
    return None

def fetch_tmdb_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        data = response.json()
        return {
            'poster': f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get('poster_path') else "",
            'overview': data.get('overview', 'No overview available'),
            'rating': data.get('vote_average', 'N/A')
        }
    except:
        return {'poster': '', 'overview': 'Error fetching details.', 'rating': 'N/A'}

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        movie_id = get_movie_id(title)
        if movie_id:
            details = fetch_tmdb_details(movie_id)
            recommendations.append((title, details['poster'], details['rating'], details['overview']))
        else:
            recommendations.append((title, '', 'N/A', 'No overview available'))
    return recommendations
