from website import create_app
from flask.cli import with_appcontext
from website.functions import DBAdditions
import click
import validators

# Call the function to create the Flask app instance
app = create_app()

#cd to where main is in cmd, then run: flask --app main populatemovies https://editorial.rottentomatoes.com/guide/best-2023-movies/ 2023
#also, this is just a test run of the code, please dont add the same year multiple times, plus it really only works for rotten tomatoes and some other sites,
#currently, the scraper just grabs things that are h2 <a> links (which is something many sites do to link to imdb)
@app.cli.command('populatemovies')
@click.argument('url')
@click.argument('year')
@with_appcontext
def add_movies_command(url, year): 
    if not validators.url(url):
        print("invalid Url")
    else:
        movie_titles = DBAdditions.extract_movie_titles(url)
        DBAdditions.add_movies(movie_titles, year)
        print("finished")

if __name__ == "__main__":
    app.run(debug=True, port=5008)

