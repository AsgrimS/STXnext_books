import pytest
from datetime import datetime
from decimal import Decimal

from books.utils import (
    parse_date,
    get_books,
    create_and_save_book,
    create_and_add_authors,
    create_and_add_categories,
)
from books.models import Book, Author, Category


@pytest.mark.parametrize(
    "value, expected",
    (("2000", "2000-01-01"), ("1990-06", "1990-06-01"), ("1854-10-12", "1854-10-12"), ("199?-03-02", "1990-03-02"),),
)
def test_parse_date(value, expected):
    assert parse_date(value) == expected


def test_get_books(requests_mock):
    value = "test_value"
    pagination_size = "test_number"
    start_index = "test_index"
    requests_mock.get(
        f"https://www.googleapis.com/books/v1/volumes?q={value}&maxResults={pagination_size}&startIndex={start_index}",
        json={"items": "test_items"},
    )

    response = get_books(value, pagination_size, start_index)
    assert response == "test_items"


@pytest.mark.django_db
def test_create_and_add_authors():
    test_authors = ["John Test", "Bob Test"]
    different_test_author = "Sam Smith"
    Author.objects.create(name=test_authors[0])
    Author.objects.create(name=different_test_author)

    test_book_id = "123456"
    test_book = Book(
        book_id=test_book_id,
        title="Test",
        published_date="2020-01-01",
        average_rating="2.1",
        ratings_count=21,
        thumbnail="http:/test",
    )
    test_book.save()
    create_and_add_authors(authors=test_authors, book_instance=test_book)
    book = Book.objects.get(book_id=test_book_id)
    assert book.authors.count() == 2
    assert Author.objects.count() == 3


@pytest.mark.django_db
def test_create_and_add_categories():
    test_categories = ["Fantasy", "Bilbo", "Unicorns"]
    different_test_category = "Dragons"
    Category.objects.create(tag=test_categories[0])
    Category.objects.create(tag=different_test_category)

    test_book_id = "123456"
    test_book = Book(
        book_id=test_book_id,
        title="Test",
        published_date="2020-01-01",
        average_rating="2.1",
        ratings_count=21,
        thumbnail="http:/test",
    )
    test_book.save()
    create_and_add_categories(categories=test_categories, book_instance=test_book)
    book = Book.objects.get(book_id=test_book_id)
    assert book.categories.count() == 3
    assert Category.objects.count() == 4


@pytest.mark.django_db
def test_create_and_save_book():

    test_id = "123456"
    test_titile = "TestTitle"
    test_published_date = "2020-01-01"
    test_average_rating = "2.1"
    test_rating_count = 21
    test_img_url = "http/image"

    test_book_json = {
        "id": test_id,
        "volumeInfo": {
            "title": test_titile,
            "publishedDate": test_published_date,
            "averageRating": test_average_rating,
            "ratingsCount": test_rating_count,
            "imageLinks": {"thumbnail": test_img_url},
        },
    }
    create_and_save_book(book=test_book_json)
    book = Book.objects.get(book_id=test_id)

    assert book.book_id == test_id
    assert book.title == test_titile
    assert book.published_date == datetime(2020, 1, 1).date()
    assert book.average_rating == Decimal(test_average_rating)
    assert book.ratings_count == test_rating_count
    assert book.thumbnail == test_img_url
    assert Book.objects.count() == 1
