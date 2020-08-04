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
from books.models import Book


@pytest.mark.parametrize(
    "value, expected",
    (("2000", "2000-01-01"), ("1990-06", "1990-06-01"), ("1854-10-12", "1854-10-12")),
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
def test_create_and_add_authors_and_categories():
    test_authors = ["John Test", "Bob Test"]
    test_categories = ["Fantasy", "Bilbo", "Unicorns"]
    test_book = Book(
        book_id="123456",
        title="Test",
        published_date="2020-01-01",
        average_rating="2.1",
        ratings_count=21,
        thumbnail="http:/test",
    )
    test_book.save()

    create_and_add_authors(authors=test_authors, book_instance=test_book)
    create_and_add_categories(categories=test_categories, book_instance=test_book)

    book = Book.objects.get(book_id="123456")

    assert book.authors.count() == 2
    assert book.categories.count() == 3


@pytest.mark.django_db
def test_create_and_save_book():
    test_book_json = {
        "id": "123456",
        "volumeInfo": {
            "title": "TestTitle",
            "publishedDate": "2020-01-01",
            "averageRating": "2.1",
            "ratingsCount": 21,
            "imageLinks": {"thumbnail": "http/image"},
        },
    }
    create_and_save_book(book=test_book_json)
    book = Book.objects.get(book_id="123456")

    assert book.book_id == "123456"
    assert book.title == "TestTitle"
    assert book.published_date == datetime(2020, 1, 1).date()
    assert book.average_rating == Decimal("2.1")
    assert book.ratings_count == 21
    assert book.thumbnail == "http/image"
    assert Book.objects.count() == 1
