import pandas as pd
import numpy as np
from difflib import get_close_matches
import pickle
import bz2


MODEL = "./flask_app/model/nmf_nc1000_max_iter500.pbz2"
DATA_PATH = "./flask_app/data/"
R_col = pd.read_csv(DATA_PATH+'R_col_small.csv')
R_col.columns = R_col.columns.astype(int)
movies = pd.read_csv(DATA_PATH+'movies_year.csv',
                     sep=";", index_col='movieId')
new_user_id = R_col.index.max()+1

def title_to_movieid(title):
    movie = get_close_matches(title, movies['title'], n=1, cutoff=0.6)
    try:
        movie_id = movies.index[movies['title'] == movie[0]].tolist()[0]

    except:
        movie_id = None
        print(f"Movie {title} not found!")
    return movie_id, movie

def movieid_to_title(id_list):
    recommendations = []
    for movie_id in id_list:
        title = movies.at[movie_id, 'title']

        recommendations.append((title, movie_id))
    return recommendations

def make_user_frame(query, R_col):
    new_user = np.zeros(shape=(1, len(R_col.columns))).tolist()[0]
    idquery = {}
    for key in query.keys():
        movie_id, movie_ = title_to_movieid(key)
        idquery[movie_id] = query[key]

    for index, movie_id in enumerate(R_col.columns):
        if movie_id in idquery.keys():
            print(movie_id)
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
    Q = pd.DataFrame(nmf.components_, columns=R_col.columns)
    # generate a dataframe with query-data, similar to "ratings"
    user_frame, idquery = make_user_frame(query, R_col)  
    P_new = nmf.transform(user_frame)
    R_new = np.dot(P_new, Q)
    R_hat = pd.DataFrame(R_new,
                         index=[new_user_id],
                        columns=R_col.columns)
    # drop movies of the query
    R_hat.drop(list(idquery.keys()), axis=1, inplace=True)
    # make a sorted list of recommended movies
    R_hat_top = R_hat.transpose().sort_values(by=[new_user_id], axis=0, ascending=False).head(k) 

    return movieid_to_title(list(R_hat_top.index))
