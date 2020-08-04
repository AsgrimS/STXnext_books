from rest_framework import serializers

from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["tag"]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = [
            "title",
            "authors",
            "published_date",
            "categories",
            "average_rating",
            "ratings_count",
            "thumbnail",
        ]


class DbUpdateSerializer(serializers.Serializer):
    q = serializers.CharField(required=True)
