'''https://developers.themoviedb.org/3/movies/get-movie-details'''
'''Get information from TMDB with APIv3:
- title
- overview
- poster_path
- vote_average (rating)
- release_date
'''
from tmdbv3api import Movie

class TMDBInfo:

    def __init__(self, movieId, api_key):
        self.language = 'en'
        self.base = "https://api.themoviedb.org/3/movie/"
        self.append_to_response = "videos"
        self.key = []
        self.name = []
        self.site = []
        self.movieId = movieId
        self.api_key = api_key

    def get_details(self):
        """
        Get movie details from TMDb
        """
        movieId = self.movieId
        movie = Movie()
        try:
            m = movie.details(movieId)
            overview = getattr(m, 'overview', None)
            title = getattr(m, 'title', None)
            vote_average = getattr(m, 'vote_average', None)
            release_date = getattr(m, 'release_date', None)
            poster = getattr(m, 'poster_path', None)
            image_base = 'http://image.tmdb.org/t/p/w500/'
            image_url = image_base+poster
        except:
            return None,None,None,None,None

        return overview, image_url, title, vote_average, release_date
