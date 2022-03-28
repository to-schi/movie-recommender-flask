from sklearn.decomposition import NMF
import pandas as pd
import joblib
import bz2
import pickle
from time import time, ctime
import logging

start = time()
logging.critical(f"starting {ctime(start)}")

#open dataframe
ratings = pd.read_csv('./flask_app/data/ratings.csv')
ratings = ratings.drop(columns=['timestamp'])

#set parameters
n_components = 1000
max_iter = 500

def compressed_pickle(data, filename):
    with bz2.BZ2File(filename + '.pbz2', 'w') as f:
        pickle.dump(data, f)

def prepare_data(data):
    ratings_wide = pd.pivot_table(
        data, index='userId', columns='movieId', values='rating')
    ratings_wide = ratings_wide.fillna(0)

    ratings_wide.to_csv(f"./R_small.csv", index=None)
    logging.critical("R_small.csv saved.")
    R_empty = ratings_wide[0:0]
    R_empty.to_csv(f"./R_col_small.csv", index=None)
    logging.critical("R_col_small.csv saved.")
    return ratings_wide

def train_nmf(data, n_components=n_components, max_iter=max_iter):
    # train and save NMF-model
    R = prepare_data(data)
    nmf = NMF(n_components=n_components,
            init='random',
            random_state=10,
            max_iter=max_iter,
            )
    nmf.fit(R)

    compressed_pickle(nmf, f"nmf_nc{n_components}_max_iter{max_iter}")
    logging.critical("Compressed pickle saved.")
    joblib.dump(nmf, f"nmf_nc{n_components}_max_iter{max_iter}.sav")
    logging.critical("binary model saved.")

    error = nmf.reconstruction_err_
    logging.critical(f"Reconstruction error: {error}")

    with open("./error.txt", 'a') as file:
        file.write(
            f"n_components: {n_components}, max_iter: {max_iter}, error: {error}"
            )

train_nmf(ratings)

end = time()
logging.critical(f"Finished {ctime(end)}")
