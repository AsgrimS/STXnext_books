from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Book
from .serializers import BookSerializer, QSerializer
from . import utils


class BookViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin ,GenericViewSet):

    serializer_class = BookSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = Book.objects.all()

        published_date = self.request.query_params.get("published_date", None)
        author = self.request.query_params.get("author", None)
        sort_by = self.request.query_params.get("sort", None)

        if published_date is not None:
            if not published_date.isnumeric():
                raise ValidationError(detail="date must be numeric" ,code=400)
            queryset = queryset.filter(published_date__year=published_date)

        if author is not None:
            queryset = queryset.filter(authors__name=author)

        if sort_by == "published_date":
            queryset = queryset.order_by("published_date")
        elif sort_by == "-published_date":
            queryset = queryset.order_by("-published_date")

        return queryset

class PostBookView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = QSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        value = serializer.data["q"]
        utils.updateDataBase(value)
        return Response("ok")
