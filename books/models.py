from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Author(models.Model):
    name = models.TextField(unique=True) # Using text fields....
    def __str__(self):
        return self.name
    
class Category(models.Model):
    tag = models.TextField(unique=True)
    def __str__(self):
        return self.tag
    

#Since data in google API is not consistent across all the books and some of them lack fields like rating/authors etc.. 
class Book(models.Model):
    book_id = models.TextField(primary_key=True, editable=False)
    title = models.TextField()
    authors = models.ManyToManyField("books.Author")
    published_date = models.DateField(null=True)
    categories = models.ManyToManyField("books.Category")
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    ratings_count = models.IntegerField(null=True)
    thumbnail = models.URLField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")