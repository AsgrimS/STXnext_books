from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    # Using text fields because maximum number of characters is unknown
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")


class Category(models.Model):
    tag = models.TextField(unique=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


# Since data in google API is not consistent across all books and some of them lack fields like
# rating/authors etc.. part of the fields are null-able
class Book(models.Model):
    book_id = models.TextField(primary_key=True, editable=False)  # Using ID of book from google's api as a primary key
    title = models.TextField(null=True)
    authors = models.ManyToManyField("books.Author", null=True)
    published_date = models.DateField(null=True)
    categories = models.ManyToManyField("books.Category", null=True)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    ratings_count = models.IntegerField(null=True)
    thumbnail = models.URLField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
