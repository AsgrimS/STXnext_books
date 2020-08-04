from rest_framework import routers
from django.urls import path

from .views import BookViewSet, PostBookView

app_name = 'books'

router = routers.DefaultRouter()

router.register('', BookViewSet, "books")


urlpatterns = [path("db/", PostBookView.as_view(), name="db")] + router.urls
