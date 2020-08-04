import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_BookViewSet(client):
    url = reverse("api:books:books-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_BbUpdateView(client):
    response = client.post(reverse("api:books:db"), {"q": "war"})
    assert response.status_code == 200

