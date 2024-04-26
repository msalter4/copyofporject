# store the standard routes for the website 
from flask import Blueprint, render_template, request, session, redirect, url_for
from . import db
# Blueprint is a way to seperate the app out for all of the views into different files
from flask_login import login_required, current_user
from .models import Recommendation, WatchedMovie
from .functions import QuizFunctions, MovieCards, DBAdditions

#set up a blueprint for the flask application
views = Blueprint('views', __name__) 

# create a route 
@views.route('/')
@views.route('/home')
@login_required
#Changed this ****
def home():
    user_id = current_user.id
    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required	
def profile():

    user_id = current_user.id
    # this returns a list of all recommendations
    recommendations = Recommendation.query.filter_by(user_id=user_id).all()
    # this returns a list of all watched movies
    watched_movies = WatchedMovie.query.filter_by(user_id=user_id).all()
    
    # MovieCard Function to print all of the movies
    # we will be storing the movies in a list of dictionaries
    if request.method == 'POST':
        selected_recommendations = request.form.getlist('recommendations')
        for recommendation_id in selected_recommendations:
            recommendation = Recommendation.query.get(recommendation_id)
            if recommendation:
                watched_movie = WatchedMovie(user_id=user_id, movie_id=recommendation.movie_id)
                db.session.add(watched_movie)

        db.session.commit()
        
    #Changed***
    return render_template('profile.html',recommendations=recommendations, watched_movies=watched_movies )
	
	
@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    return render_template('quiz.html', user=current_user)

@views.route('/quizsimilar', methods=['GET', 'POST'])
@login_required
def quiz_similar():
    #function needs alot of cleaning along with the attached methods
    user_id = current_user.id 
    if 'thirty_recommendations' not in session:
        session['thirty_recommendations'] = []
    if 'tempr' not in session:
        session['tempr'] = []
   
    thirty_recommendations = session['thirty_recommendations']
    tempr = session['tempr']
    if thirty_recommendations == 0 or len(tempr) < 10:
        thirty_recommendations = QuizFunctions.generate_similar_quiz_results(user_id)
        tempr = thirty_recommendations[:10]

    if request.method == 'POST':
        watched_items = []
        not_interested_items = []
        for key in request.form.keys():
            if key.startswith('w'):
                watched_items.append(int(request.form[key]))
            elif key.startswith('ni'):
                not_interested_items.append(int(request.form[key]))
        print("Tmpr:", tempr)
        print("thrity:", thirty_recommendations)
        print("Watched Items:", watched_items)
        print("Not Interested Items:", not_interested_items)
        for movie_id in watched_items:
            if watched_items is not None:
                DBAdditions.add_watched(user_id, movie_id)
                tempr.remove(movie_id)
                thirty_recommendations.remove(movie_id)
        print("Tmpr:", tempr)
        print("thrity:", thirty_recommendations)

        for movie_id in not_interested_items:
            if movie_id is not None:
                thirty_recommendations.remove(movie_id)
                tempr.remove(movie_id)

        if not (watched_items or not_interested_items):
            for t in tempr:
                new_recommendation = Recommendation(user_id = user_id, movie_id = t)
                db.session.add(new_recommendation)
            db.session.commit()
            return redirect(url_for('views.home'))

    t = MovieCards.remove_watched_ids(tempr, user_id)
    MovieCards.display_information(t)
    displayed = MovieCards.display_information(t)
    session['thirty_recommendations'] = thirty_recommendations
    session['tempr'] = tempr
    return render_template('quizsimilar.html', user=current_user, displayed=displayed)
 
@views.route('/newquiz', methods=['GET', 'POST'])
@login_required
def quiz_new():
    user_id = current_user.id
    if request.method == 'POST':
        pass

    return render_template('newquiz.html', user=current_user)

