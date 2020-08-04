from rest_framework import routers
from django.urls import path

from .views import BookViewSet, QBookView

app_name = "books"

router = routers.DefaultRouter()

router.register("", BookViewSet, "books")


urlpatterns = [path("db/", QBookView.as_view(), name="db")] + router.urls
