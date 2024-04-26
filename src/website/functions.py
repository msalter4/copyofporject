from lib2to3.pytree import WildcardPattern
from .models import Actor, Genre, Director, Movies, Writer, Language, Recommendation, WatchedMovie
from imdb import Cinemagoer
from sqlalchemy import and_
from . import db
import requests
from bs4 import BeautifulSoup

class QuizFunctions():
    def generate_similar_quiz_results(user_id):
        watched_ids = [watched.movie_id for watched in WatchedMovie.query.filter_by(user_id=user_id).all()]
        recommendations = [recommendation.movie_id for recommendation in Recommendation.query.filter_by(user_id=user_id).all()]
        genre_list = []
        actor_list = []
        director_list = []

        for movie_id in watched_ids:
            temp = Genre.query.filter_by(movie_id=movie_id).all()
            temp1 = Actor.query.filter_by(movie_id=movie_id).all()
            temp2 = Director.query.filter_by(movie_id=movie_id).all()
            for t in temp:
                genre_list.append(t.genre)
            for a in temp1:
                actor_list.append(a.actor)
            for b in temp2:
                director_list.append(b.director)
        genre_list = list(set(genre_list))
        actor_list = list(set(actor_list))
        director_list = list(set(director_list))
        """number_of_occurences = {}
        number_of_occurences1 = {}
        number_of_occurences2 = {}

        for genre, actor, director in genre_list, actor_list, director_list:
            if genre in number_of_occurences:
                number_of_occurences[genre] += 1
            else:
                number_of_occurences[genre] = 1


            if actor in number_of_occurences1:
                number_of_occurences1[actor] += 1
            else:
                number_of_occurences1[actor] = 1


            if actor in number_of_occurences2:
                number_of_occurences2[director] += 1
            else:
                number_of_occurences2[director] = 1"""


        #if key genre in numoccurance < .05 * numwatchedmovies:
         #   remove the genre from genrelist

        movies_query = Movies.query \
            .join(Director) \
            .join(Genre) \
            .join(Actor)

        if director_list and genre_list and actor_list:
            result_query = movies_query.filter(
                and_(
                    Director.director.in_(director_list),
                    Genre.genre.in_(genre_list),
                    Actor.actor.in_(actor_list)
                )
            )
        filtered_movie_ids = [movie.movie_id for movie in result_query.all()]
        initial = [movie_id for movie_id in filtered_movie_ids if movie_id not in watched_ids]
        if len(filtered_movie_ids) < 30:
            if director_list and genre_list and actor_list:
                result_query = movies_query.filter(
                    and_(
                        Director.director.in_(director_list),
                        Genre.genre.in_(genre_list)
                    )
                )
                result_query1 = movies_query.filter(
                    and_(
                        Director.director.in_(director_list),
                        Actor.actor.in_(actor_list)
                    )
                )

            a = [movie.movie_id for movie in result_query.all()]
            b = [movie.movie_id for movie in result_query1.all()]
            filtered_movie_ids = a + b
            final = [movie_id for movie_id in filtered_movie_ids if movie_id not in watched_ids]


        

        return final + initial

            
   
class DBAdditions():
    def extract_movie_titles(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            h2_tags = soup.find_all('h2')
            movie_titles = []
            for tag in h2_tags:
                a_tags = tag.find_all('a')
                if a_tags:
                    for a_tag in a_tags:
                        movie_title = a_tag.get_text().strip()
                        if movie_title:
                            movie_titles.append(movie_title)
            return movie_titles    
        except Exception as e:
            print(e)
            return

    def add_movies(titles, year):
        ia = Cinemagoer()
        for title in titles:
            if Movies.query.filter_by(title=title, year=year).first():
                print(title, " already exists")

            else:
                movie = ia.search_movie(title)[0]
                ia.update(movie)
                tid = movie.movieID
                if movie['kind'] == 'movie':
                    if tid and movie.get('full-size cover url') is not None:
                        new_movie = Movies(movie_id = tid, title=title, url=movie['full-size cover url'], year=year)
                        db.session.add(new_movie)
                    elif tid and movie.get('full-size cover url') is None:
                        new_movie = Movies(movie_id = tid, title=title, url=None, year=year)
                        db.session.add(new_movie)

                    if 'genres' in movie: 
                        for genre in movie['genres']:
                            if(genre):
                                new_genre = Genre(movie_id = tid, genre=genre)
                                db.session.add(new_genre)
                    else:
                        print(title, " doesnt have genres")

                    if 'languages' in movie: 
                        for language in movie['languages']:
                            if(language):
                                new_language = Language(movie_id = tid, language=language)
                                db.session.add(new_language)
                    else:
                        print(title, " doesnt have languages")

                    if 'director' in movie:
                        for director in movie['director'][:2]:
                            if director:
                                new_director = Director(movie_id=tid, director=director['name'])
                                db.session.add(new_director)  
                    else:
                        print(title, " doesn't have directors")

                    if 'writer' in movie: 
                        for writer in movie['writers'][:2]:
                            if(writer):
                                new_writer = Writer(movie_id = tid, writer=writer['name'])
                                db.session.add(new_writer)
                    else:
                        print(title, " doesnt have writers")

                    if 'cast' in movie:
                        for actor in movie['cast'][:8]:
                            if actor:
                                new_actor = Actor(movie_id=tid, actor=actor['name'])
                                db.session.add(new_actor)
                    else:
                        print(title, " doesnt have cast")
                    db.session.commit()

    def add_watched(user_id, movie_id):
        #if it exists filter
        new_watched_movie = WatchedMovie(user_id = user_id, movie_id=movie_id)
        db.session.add(new_watched_movie)
        db.session.commit()

class MovieCards():
    def display_information(movie_id_list):
        returned_info = {}
        for tid in movie_id_list:
            temp = Movies.query.filter_by(movie_id=tid).first()
            movie_info = {
                "movie_id": temp.movie_id,
                "title": temp.title,
                "url": temp.url,
                "year": temp.year
            }
            returned_info[tid] = movie_info
        return returned_info

    def remove_watched_ids(movie_id_list, user_id):
        watched_ids = [watched.movie_id for watched in WatchedMovie.query.filter_by(user_id=user_id).all()]
        new = [movie_id for movie_id in movie_id_list if movie_id not in watched_ids]
        return new

        
