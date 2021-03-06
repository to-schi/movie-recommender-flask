from flask import Flask, render_template, request, session
from flask_app.recommender import nmf_recommender, title_to_movieid
from flask_app.get_TMDB import TMDBInfo
from flask_app.tmdb_config import API_KEY
from tmdbv3api import TMDb
import pandas as pd
import logging
import os


app = Flask(import_name=__name__)
app.secret_key = os.urandom(12).hex()
# initiate TMDB-API
tmdb = TMDb()
tmdb.api_key = API_KEY
links = pd.read_csv('./flask_app/data/links.csv', index_col='movieId')

@app.route("/")
def home():
    return render_template('home.html')

def make_movie_info(movie_ids):
    movie_info = pd.DataFrame(
        columns=["title", "overview", "image_url", "average_rating", "release_date"])
    # Get TMDB-movie_ids from "links.csv"
    for i in movie_ids:
        if i != None:
            tmdb_id = links.at[i, 'tmdbId']
            t = TMDBInfo(movieId=tmdb_id, api_key=tmdb.api_key)
            overview, image_url, title, average_rating, release_date = t.get_details()
            movie_link = 'https://www.themoviedb.org/movie/'+str(tmdb_id)
            if overview == None:
                continue
            else:
                tmdb_data = {"title": title, "overview": overview, "image_url": image_url, "average_rating": average_rating,
                             "release_date": release_date, "link": movie_link}
                movie_info = pd.concat(
                    [movie_info, pd.DataFrame.from_records([tmdb_data])], ignore_index=True)
        # If title_to_movieid finds no match and returns "None", no info will be displayed:
        else:
            movie_info[i] = ""
    return movie_info

@app.route("/check")
def check():
    # Get values from server request-url (user-input)
    request_dict = request.args.to_dict()
    input_list = list(request_dict.values())
    # Save input in session-variable for later use in function def result():
    session['input_list'] = input_list
    logging.critical(f"check Input: {session['input_list']}")
    # Get movie-id-list from input
    movie_id_list = []
    for title in input_list:
        if title == "":
            continue
        else:
            movie_id = title_to_movieid(title)
            movie_id_list.append(movie_id)
    # Get movie-information from TMDb:
    movie_info = make_movie_info(movie_id_list)

    return render_template(
        'check.html',
        my_title="reliable recommender",
        movie_info=movie_info)


@app.route("/recommendation")
def result():
    # get values from server request-url (user-input)
    try:
        input_list = session.get('input_list', None)
        logging.critical(f"recommendation INPUT: {input_list}")
    except:
        logging.critical(f"recommendation INPUT: None")
        return home()

    # movie-list is transformed into a query-dictionary with an
    # automatic rating-value "5" for every favorite movie in the list:
    query = {}
    for movie in input_list:
        if movie == "":
            continue
        else:
            query[movie] = 5
    # query-dict is passed into the nmf_recommender-function (recommenders-module) returning a tuple of ("title", "movie_id"):
    recom = nmf_recommender(query, 12)
    # A pandas dataframe is created to store media-data gathered from the TMDB-API:
    movie_info = make_movie_info(recom)
    logging.critical(f"movie_info: {movie_info}")
    return render_template(
        'results.html',
        my_title="reliable recommender",
        movie_info=movie_info)


if __name__ == '__main__':
    # app launches the server
    app.run(debug=False)
