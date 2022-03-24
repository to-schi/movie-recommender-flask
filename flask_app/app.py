from flask import Flask, render_template, request
from flask_app.recommender import nmf_recommender, title_to_movieid
from flask_app.get_TMDB import TMDBInfo
from flask_app.tmdb_config import API_KEY
from tmdbv3api import TMDb
import pandas as pd
import logging

app = Flask(import_name=__name__)
# initiate TMDB-API
tmdb = TMDb()
tmdb.api_key = API_KEY
DATA_PATH = "./flask_app/data/"
links = pd.read_csv(DATA_PATH+'links.csv', index_col='movieId')


@app.route("/")
def home():
    return render_template('home.html')


def make_movie_info(movie_ids):
    movie_info = pd.DataFrame(
        columns=["title", "overview", "image_url", "average_rating", "release_date"])
    # Get TMDB-movie_ids from "links.csv"
    for i in movie_ids:
        try:
            # for the recommender-dictionary
            tmdb_id = links.at[i[1], 'tmdbId']
        except:
            # for the movie_id-list
            tmdb_id = links.at[i, 'tmdbId']

        t = TMDBInfo(movieId=tmdb_id, api_key=tmdb.api_key, tmdb=tmdb)
        overview, image_url, title, average_rating, release_date = t.get_details()
        movie_link = 'https://www.themoviedb.org/movie/'+str(tmdb_id)
        if overview == "empty":
            continue
        else:
            tmdb_data = {"title": title, "overview": overview, "image_url": image_url, "average_rating": average_rating,
                         "release_date": release_date, "link": movie_link}
            movie_info = pd.concat(
                [movie_info, pd.DataFrame.from_records([tmdb_data])], ignore_index=True)
    return movie_info


@app.route("/check")
def check():
    # The input-list must be global for use in the next function (def result)
    global input_list

    # get values from server request-url (user-input)
    request_dict = request.args.to_dict()
    input_list = list(request_dict.values())

    # get movie-id-list from input
    movie_id_list = []
    for title in input_list:
        if title == "":
            continue
        else:
            movie_id, movie_ = title_to_movieid(title)
            movie_id_list.append(movie_id)
    # get movie-information from TMDb:
    movie_info = make_movie_info(movie_id_list)

    return render_template(
        'check.html',
        my_title="reliable recommender",
        movie_info=movie_info)

@app.route("/recommendation")
def result():
    # get values from server request-url (user-input)
    movie_list = input_list
    logging.critical(f"INPUT: {movie_list}")
    # movie-list is transformed into a query-dictionary with an automatic rating-value "5" for every favorite movie in the list:
    query = {}
    for movie in movie_list:
        if movie == "":
            continue
        else:
            query[movie] = 5
    # query-dict is passed into the nmf_recommender-function (recommenders-module):
    recom = nmf_recommender(query, 12)
    # A pandas dataframe is created to store media-data gathered from the TMDB-API:
    movie_info = make_movie_info(recom)

    return render_template(
        'results.html',
        my_title="reliable recommender",
        movie_info=movie_info)


if __name__ == '__main__':
    # app launches the server
    app.run(debug=False)
