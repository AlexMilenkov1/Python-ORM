import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models


def find_books_by_genre_and_language(book_genre, language):
    searched_books = Book.objects.filter(genre=book_genre, language=language)

    return searched_books


def find_authors_nationalities():
    authors = Author.objects.filter(nationality__isnull=False)

    result = [f"{a.first_name} {a.last_name} is {a.nationality}" for a in authors]

    return '\n'.join(result)

def order_books_by_year():
    ordered_books = Book.objects.order_by('publication_year', 'title')

    result = [f"{b.publication_year} year: {b.title} by {b.author}" for b in ordered_books]

    return '\n'.join(result)

def delete_review_by_id(reviewer_id: int):
    targeted_reviewer = Review.objects.get(id=reviewer_id)

    targeted_reviewer.delete()

    return f"Review by {targeted_reviewer.reviewer_name} was deleted"

def filter_authors_by_nationalities(nationality):
    result = []

    filtered_authors = Author.objects.filter(nationality=nationality).order_by('first_name', 'last_name')

    for author in filtered_authors:
        if author.biography:
            result.append(author.biography)
        else:
            result.append(f"{author.first_name} {author.last_name}")

    return '\n'.join(result)

def filter_authors_by_birth_year(first_year, second_year):
    ordered_authors = Author.objects.filter(birth_date__year__range=(first_year, second_year)).order_by('-birth_date')

    result = [f"{a.birth_date}: {a.first_name} {a.last_name}" for a in ordered_authors]

    return '\n'.join(result)


def change_reviewer_name(reviewer_name, new_name):
    changed_reviewers_names = Review.objects.filter(reviewer_name=reviewer_name).update(reviewer_name=new_name)

    return Review.objects.all()
