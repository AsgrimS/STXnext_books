import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_book_view_set(client):
    url = reverse("api:books:books-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test__db_update_view(requests_mock, client):
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
    requests_mock.get(
        "https://www.googleapis.com/books/v1/volumes?q=war&maxResults=40&startIndex=0",
        json={"items": [test_book_json]},
    )
    response = client.post(reverse("api:books:db"), {"q": "war"})
    assert response.status_code == 200
