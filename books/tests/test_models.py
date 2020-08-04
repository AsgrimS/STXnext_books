import pytest

from books.models import Author, Category, Book


@pytest.mark.django_db
def test_author_create():
    Author.objects.get_or_create(name="John Test")
    assert Author.objects.count() == 1


@pytest.mark.django_db
def test_category_create():
    Category.objects.get_or_create(tag="Fantasy")
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_book_create():
    Book.objects.get_or_create(
        book_id="123456",
        title="Test",
        published_date="2020-01-01",
        average_rating="2.1",
        ratings_count=21,
        thumbnail="http:/test",
    )
    assert Book.objects.count() == 1
