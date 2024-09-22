import pandas as pd
import numpy as np

movies = pd.read_csv(r'./Movies/tmdb_5000_movies.csv')
credits = pd.read_csv(r'./Movies/tmdb_5000_credits.csv')

movies = movies.merge(credits, on='title')
# print(movies.head())

movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

movies = movies.dropna()
empty = movies.isnull().sum()
duplicated = movies.duplicated().sum()
print(empty)
print("Duplicated",duplicated)
#geners
# id
# keywords
# title
# overview
# Cast
# crew