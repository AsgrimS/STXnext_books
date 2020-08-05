import re

from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Book
from .serializers import BookSerializer, DbUpdateSerializer
from . import utils


class BookViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

    serializer_class = BookSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = Book.objects.all()

        published_date = self.request.query_params.get("published_date", None)
        author = self.request.query_params.get("author", None)
        sort_by = self.request.query_params.get("sort", None)

        allowed_sort_by = {"published_date", "-published_date"}

        if published_date is not None:

            if not re.match(r"^\d{4}$", published_date):
                raise ValidationError(
                    "Value for published date has to be year (4 digits)"
                )

            queryset = queryset.filter(published_date__year=published_date)

        if author is not None:
            queryset = queryset.filter(authors__name=author)

        if sort_by in allowed_sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset


class DbUpdateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = DbUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        value = serializer.data["q"]
        utils.update_database(
            value, logging=False
        )  # In order to see progress bars like when using update_database command, change loggin to True

        return Response("Database Updated")
