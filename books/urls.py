from rest_framework import routers
from django.urls import path

from .views import BookViewSet, DbUpdateView

app_name = "books"

router = routers.DefaultRouter()

router.register("books", BookViewSet, "books")


urlpatterns = [path("db", DbUpdateView.as_view(), name="db")] + router.urls
