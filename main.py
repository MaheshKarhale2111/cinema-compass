import streamlit as st 
import pandas as pd 
import pickle


import requests

def fetch_movie(id):
    url = "https://api.themoviedb.org/3/movie/{id}?api_key=3aff4a4c64c4c043e73ab676a717e5d0"

    try:
        response = requests.get(url.format(id =id))
        response.raise_for_status()

        return response.json()["poster_path"]

    except requests.exceptions.HTTPError as http_err:
        pass
        # st.error(f"TMDB api is down")
    
    except requests.exceptions.ConnectionError as conn_err:
        pass
        # st.error(f"TMDB api is down")
    
    return "nullposterpath"



movies = pd.read_csv('movies_list.csv')
movie_list = movies['title'].tolist()
st.subheader('Select a movie')
selected_movie = st.selectbox(' ',movie_list)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    # by sorting we are losing index postion of movie , call enumerate
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]
    recommended_movie_index = []
    recommended_movie  = []
    for i in movies_list:

        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_index.append(movies.iloc[i[0]].movie_id)
    # return movies_list
    return recommended_movie, recommended_movie_index


st.sidebar.header("CINEMA COMPASS") 
st.sidebar.text("A MOVIE RECOMMENDATION SYSTEM") 
# st.sidebar.divider()
st.sidebar.markdown(''' **:red-background[How it works?]**''')
st.sidebar.markdown('''Select a movie from the dropdown and click 'Recommend' to get the top 5 movie recommendations.''')
st.sidebar.markdown(''' **:red-background[How it's made?]**''')
st.sidebar.markdown('''Model is trained with top 5000 movies from TMDB dataset''')
st.sidebar.markdown(''' **:red-background[Movie name is visible but can't see poster?]**''')
st.sidebar.markdown('''That's error from TMDB api, Try again after few seconds''')


if st.button("Recommmend"):
    # st.write("Why hello there")
    movie_indexes = recommend(selected_movie)
    posters = []

    movies, indexes = recommend(selected_movie)

    for i in indexes:
        poster_path = fetch_movie(i)
        if(poster_path == "nullposterpath"):
            posters.append('fetch_fail.png')
        else:
             posters.append("https://image.tmdb.org/t/p/w500/"+poster_path)

        
    
    # st.divider()



    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h4 style='padding: 1rem 5px 1rem 5px'>{movies[0]}</h4>", unsafe_allow_html=True)
        st.image(posters[0])
    with col2:
        st.markdown(f"<h4 style='padding: 1rem 5px 1rem 5px'>{movies[1]}</h4>", unsafe_allow_html=True)
        st.image(posters[1])
    
    
    col1, col2, col3 = st.columns(3)

    with col1:
        # st.subheader(f'''**{movies[2]}**''')
        st.markdown(f"<h5 style='padding: 1rem 5px 10px 5px'>{movies[2]}</h5>", unsafe_allow_html=True)
        st.image(posters[2])
    with col2:
        st.markdown(f"<h5 style='padding: 1rem  5px 10px 5px''>{movies[3]}</h5>", unsafe_allow_html=True)
        st.image(posters[3])
    with col3:
        st.markdown(f"<h5 style='padding: 1rem  5px 10px 5px''>{movies[4]}</h5>", unsafe_allow_html=True)
        st.image(posters[4],)
   

    

    
