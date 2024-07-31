import os
import django
from django.db.models import Q, Count, Avg, Max, F
import random
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie


# Create queries within functions
def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    name_query = Q(full_name__icontains=search_name)
    nationality_query = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = (name_query & nationality_query)
    elif search_name is not None:
        query = name_query
    else:
        query = nationality_query

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = []

    for d in directors:
        result.append(f'Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}')

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."


def get_top_actor():
    top_actor = (Actor.objects
                 .prefetch_related('starring_movies')
                 .annotate(movies_count=Count('starring_movies'), avg_rating=Avg('starring_movies__rating'))
                 .order_by('-movies_count', 'full_name')
                 .first()
    )

    if not top_actor or not top_actor.movies_count:
        return ''

    movies = top_actor.starring_movies.all()

    movies_titles = ', '.join(movie.title for movie in movies)

    return f"Top Actor: {top_actor.full_name}, starring in movies: {movies_titles}, movies average rating: {top_actor.avg_rating:.1f}"


def get_actors_by_movies_count():
    most_participated_actors = (Actor
                                .objects
                                .prefetch_related('movies')
                                .annotate(movies_count=Count('movies'))
                                .order_by('-movies_count', 'full_name'))

    result = []

    if not most_participated_actors or not most_participated_actors[0].movies_count:
        return ''
    elif len(most_participated_actors) < 3:
        result.extend([f"{a.full_name}, participated in {a.movies_count} movies" for a in most_participated_actors])
    else:
        top_3 = most_participated_actors[:3]

        result.extend([f"{a.full_name}, participated in {a.movies_count} movies" for a in top_3])

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    highest_rating = Movie.objects.aggregate(max_rating=Max('rating'))['max_rating']

    greatest_movie = (Movie.objects
                      .prefetch_related('actors')
                      .select_related('starring_actor')
                      .filter(rating=highest_rating, is_awarded=True)
                      .order_by('-rating', 'title')
                      .first()
    )

    if not greatest_movie:
        return ''

    # This represents the cast logic
    cast = []

    all_actors = greatest_movie.actors.all().order_by('full_name')

    for a in all_actors:
        cast.append(a.full_name)

    # This represents the starring actor logic
    if not greatest_movie.starring_actor:
        current_starring_actor = 'N/A'
    else:
        current_starring_actor = greatest_movie.starring_actor.full_name

    return (f"Top rated awarded movie: {greatest_movie.title}, rating: {greatest_movie.rating:.1f}."
            f" Starring actor: {current_starring_actor}."
            f" Cast: {', '.join(cast)}.")


def increase_rating():
    movies_to_update = Movie.objects.filter(
        is_classic=True,
        rating__lt=10
    )

    if not movies_to_update:
        return "No ratings increased."

    movies_to_update.update(rating=F('rating') + 0.1)

    return f"Rating increased for {len(movies_to_update)} movies."


print(get_actors_by_movies_count())