from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm
import requests

from ...models import Book, Author, Category


class Command(BaseCommand):
    help = "Updates books database"

    def handle(self, *args, **options):

        pagination_size = 40
        book_count = pagination_size
        start_index = 0
        chunk_num = 1

        while book_count == pagination_size:
            r = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q=Hobbit&maxResults={pagination_size}&startIndex={start_index}"
            )
            book_json = r.json()
            items = book_json["items"]

            book_count = 0
            for book in items:
                book_count += 1

            start_index += book_count

            print(f"Loading #{chunk_num} chunk")

            chunk_num += 1

            for book in tqdm(items):

                book_id = book["id"]
                title = book["volumeInfo"].get("title")
                authors = book["volumeInfo"].get("authors")
                published_date = book["volumeInfo"].get("publishedDate")
                categories = book["volumeInfo"].get("categories")
                average_rating = book["volumeInfo"].get("averageRating")
                ratings_count = book["volumeInfo"].get("ratingsCount")
                thumbnail = book["volumeInfo"].get("imageLinks")

                if thumbnail is not None:
                    thumbnail = thumbnail.get(
                        "thumbnail", thumbnail.get("smallThumbnail")
                    )

                if published_date is not None:
                    published_date = published_date.strip("*")
                    if len(published_date) == 4:
                        published_date = f"{published_date}-01-01"
                    if len(published_date) == 7:
                        published_date = f"{published_date}-01"

                b = Book(
                    book_id=book_id,
                    title=title,
                    published_date=published_date,
                    average_rating=average_rating,
                    ratings_count=ratings_count,
                    thumbnail=thumbnail,
                )

                b.save()

                if categories is not None:
                    for category in categories:
                        c, _ = Category.objects.get_or_create(tag=category)
                        c.save()
                        b.categories.add(c)

                if authors is not None:
                    for author in authors:
                        a, _ = Author.objects.get_or_create(name=author)
                        a.save()
                        b.authors.add(a)

        print("-----------------")
        print("Database updated")
        print("-----------------")

