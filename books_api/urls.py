from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

api_urlpatterns = [
    path("books/", include("books.urls", namespace="books")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((api_urlpatterns, "api"), namespace="api")),
]
