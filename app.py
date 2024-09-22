import streamlit as st
import pickle
import requests 

# Function to fetch movie poster based on movie ID
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxY2ZmNDYzZDQ5ZDc1N2FkMTFlNTM2NDU2YWE2ZWJlMSIsIm5iZiI6MTcyNjk1ODA0My4zNzU5NTUsInN1YiI6IjY2NWEwZWI4NWQyMmJjMzBmMDJkNjJlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4ui48hVjrfztRYxkFVWKwUmFkXEmcW_4iNYP3qjhADI"  # Replace with your actual API key
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if 'poster_path' in data else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None

def recommend(DataFrame, movie_title):
    movie_index = DataFrame[DataFrame['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:20]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(DataFrame.iloc[i[0]])
    
    return recommended_movies

# Load the similarity matrix and movies DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('moviesPKL.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommendation System')
option = st.selectbox(
    'Which Movie do you like best?',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movies = recommend(movies, option)

    # Custom CSS for styling
    st.markdown("""
        <style>
        .movie-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: space-between;
        }
        .movie {
            flex: 1 1 calc(20% - 20px);
            margin: 10px;
            text-align: center;
        }
        img {
            width: 100px;
            height: auto;
            max-width: 100px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display recommended movies in multiple rows
    st.markdown('<div class="movie-container">', unsafe_allow_html=True)
    for movie in recommended_movies:
        st.markdown('<div class="movie">', unsafe_allow_html=True)
        st.write(movie['title'])
        
        # Fetch and display the movie poster
        poster_url = fetch_poster(movie['id'])
        if poster_url:
            st.markdown(f'<img src="{poster_url}" alt="{movie["title"]}" />', unsafe_allow_html=True)
        else:
            st.write("Poster not available.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
