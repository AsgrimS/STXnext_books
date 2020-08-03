from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from .models import Book
from .serializers import BookSerializer


class BookViewSet(mixins.ListModelMixin, GenericViewSet):

    serializer_class = BookSerializer
    permission_classes = (permissions.AllowAny,)

    def test(self, request, pk):
        print(pk)

    def get_queryset(self):
        queryset = Book.objects.all()

        published_date = self.request.query_params.get("published_date", None)
        author = self.request.query_params.get("author", None)
        sort_by = self.request.query_params.get("sort", None)

        if published_date is not None:
            queryset = queryset.filter(published_date__year=published_date)

        if author is not None:
            queryset = queryset.filter(authors__name=author)

        if sort_by == "published_date":
            queryset = queryset.order_by("published_date")

        if sort_by == "-published_date":
            queryset = queryset.order_by("-published_date")

        return queryset

