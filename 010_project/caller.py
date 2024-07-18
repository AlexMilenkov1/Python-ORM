import os
from datetime import date, timedelta, time

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car


# Create queries within functions
def show_all_authors_with_their_books():
    result = []

    authors = Author.objects.all().order_by('id')

    for author in authors:
        all_books = [b.title for b in author.book_set.all()]

        if not all_books:
            continue

        result.append(f"{author.name} has written - {', '.join(all_books)}!")

    return '\n'.join(result)


def delete_all_authors_without_books():
    authors = Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)

    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = [r.rating for r in product.reviews.all()]

    average_rating = sum(reviews) / len(reviews)

    return average_rating


def get_reviews_with_high_ratings(threshold: int):
    reviews = Review.objects.filter(rating__gte=threshold)

    return reviews


def get_products_with_no_reviews():
    products_without_reviews = Product.objects.filter(reviews__isnull=True).order_by('-name')

    return products_without_reviews


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    result = [str(l) for l in DrivingLicense.objects.all().order_by('-license_number')]

    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date):
    cutoff_date = due_date - timedelta(days=365)

    drivers_with_expired_license = Driver.objects.filter(license__issue_date__gt=cutoff_date)

    return drivers_with_expired_license


def register_car_by_owner(owner: Owner):
    not_related_registration = Registration.objects.filter(car__isnull=True).first()
    not_related_car = Car.objects.filter(registration__isnull=True).first()

    not_related_car.owner = owner
    not_related_car.save()

    not_related_registration.registration_date = date.today()
    not_related_registration.save()

    return f"Successfully registered {not_related_car.model} to {owner.name} with registration number {not_related_registration.registration_number}."

