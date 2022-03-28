# Type in your favorite movies and get matching recommendations!
### 1. Type in up to 10 of your favorite movies.
### 2. Check if the movies in the list are the correct selection.
### 3. Get recommendations according to your list.
\
[![demo](./img/reliable-recommender.gif)](https://reliable-recommender.herokuapp.com)
A demo of this app can be tested at: [reliable-recommender.herokuapp.com](https://reliable-recommender.herokuapp.com)

### How it works
The recommender uses the MovieLens dataset with 9724 movies.
It calculates 1000 hidden features of the ratings-data for all movies with "non-negative matrix factorization" and recommends items similar to the input.

[![Heroku](https://pyheroku-badge.herokuapp.com/?app=<HEROKU_APP_NAME>&path=<ROUTE>&style=<STYLE>)](https://reliable-recommender.herokuapp.com)