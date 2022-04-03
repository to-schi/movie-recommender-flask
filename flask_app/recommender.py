import pandas as pd
import numpy as np
from rapidfuzz import fuzz, process
import pickle
import bz2
import logging

MODEL = "./flask_app/model/nmf_nc500_max_iter1000.pbz2"
DATA_PATH = "./flask_app/data/"
R_col = pd.read_csv(DATA_PATH+'R_col_small.csv')
R_col.columns = R_col.columns.astype(int)
movies = pd.read_csv(DATA_PATH+'movies_year.csv',
                     sep=";", index_col='movieId')
# Generate new_user_id to add to dataframe
new_user_id = R_col.index.max()+1


def title_to_movieid(title):
    try:
        movie_, ratio_, movie_id = process.extractOne(title,movies['title'], scorer=fuzz.WRatio)
    except:
        movie_id = None
        logging.critical(f"Movie {title} not found!")
    return movie_id


def make_user_frame(query, R_col):
    new_user = np.zeros(shape=(1, len(R_col.columns))).tolist()[0]
    idquery = {}
    for key in query.keys():
        movie_id = title_to_movieid(key)
        # if title_to_movieid returns "None" entry in idquery is not made:
        if movie_id == None:
            continue
        else:
            idquery[movie_id] = query[key]
    #logging.critical(f"idquery: {idquery}")
    for index, movie_id in enumerate(R_col.columns):
        if movie_id in idquery.keys():
            new_user[index] = idquery[movie_id]

    user_frame = pd.DataFrame(
        [new_user], index=['new_user'], columns=R_col.columns)
    user_frame['userId'] = new_user_id
    user_frame.set_index('userId', inplace=True)
    return user_frame, idquery


def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data


def nmf_recommender(query, k=10):
    # load pre-trained nmf-data
    nmf = decompress_pickle(MODEL)
    # Make dataframe from loaded nmf-components with movie-ids as column-names
    Q = pd.DataFrame(nmf.components_, columns=R_col.columns)
    # generate a dataframe with query-data, similar to "ratings"
    user_frame, idquery = make_user_frame(query, R_col)
    # Calculate P-matrix for new_user:
    P_new = nmf.transform(user_frame)
    # Calculate predicted ratings-matrix for new_user as the dot-product of both:
    R_new = np.dot(P_new, Q)
    R_hat = pd.DataFrame(R_new,
                         index=[new_user_id],
                         columns=R_col.columns)
    # drop movies of the query from the DataFrame
    R_hat.drop(list(idquery.keys()), axis=1, inplace=True)
    # make a sorted list of recommended movies (ids)
    R_hat_top = R_hat.transpose().sort_values(
        by=[new_user_id], axis=0, ascending=False).head(k)
    recom = list(R_hat_top.index)
    return recom
