# Type in your favorite movies and get matching recommendations!
[![Heroku](https://github.com/dhalenok/pyheroku-badge/raw/master/img/deployed.svg)](https://reliable-recommender.herokuapp.com)

### 1. Type in up to 10 of your favorite movies.
### 2. Check if the movies in the list are the correct selection.
### 3. Get recommendations according to your list.
\
[![demo](./img/reliable-recommender.gif)](https://reliable-recommender.herokuapp.com)  
A demo of this app can be tested at: [reliable-recommender.herokuapp.com](https://reliable-recommender.herokuapp.com)

### How it works
The recommender uses the MovieLens dataset with 9724 movies.
It calculates 1000 "hidden features" of the ratings-data with ["non-negative matrix factorization"](https://en.wikipedia.org/wiki/Non-negative_matrix_factorization) - finding unnamed traits, that a group of movies might have in common. If a new user adds their ratings for selected movies, similar items will be recommended according to the inherent features. Unfortunately the movies have to already be part of the dataset, which was last updated in 9/2018.


