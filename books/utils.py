from tqdm import tqdm
import requests

from books.models import Book, Author, Category


def print_succes_message():
    print("-----------------")
    print("Database updated")
    print("-----------------")


def get_books(value, pagination_size, start_index):
    r = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={value}&maxResults={pagination_size}&startIndex={start_index}"
    )
    book_json = r.json()
    items = book_json["items"]
    return items


def create_and_add_authors(authors, book_instance):
    if authors is not None:
        for author in authors:
            a, _ = Author.objects.get_or_create(name=author)
            a.save()
            book_instance.authors.add(a)


def create_and_add_categories(categories, book_instance):
    if categories is not None:
        for category in categories:
            c, _ = Category.objects.get_or_create(tag=category)
            c.save()
            book_instance.categories.add(c)


# published dates vary in format on the google api. This function makes sure that all dates are converted to the YYYY-MM-DD format
def verify_date(date):
    if date is not None:
        date = date.strip("*")
        if len(date) == 4:
            date = f"{date}-01-01"
        if len(date) == 7:
            date = f"{date}-01"
    return date


def create_and_save_book(book):
    book_id = book["id"]
    title = book["volumeInfo"].get("title")
    authors = book["volumeInfo"].get("authors")
    published_date = book["volumeInfo"].get("publishedDate")
    categories = book["volumeInfo"].get("categories")
    average_rating = book["volumeInfo"].get("averageRating")
    ratings_count = book["volumeInfo"].get("ratingsCount")
    thumbnail = book["volumeInfo"].get("imageLinks")

    # If there is a thumbnail, normal has higher priority over small
    if thumbnail is not None:
        thumbnail = thumbnail.get("thumbnail", thumbnail.get("smallThumbnail"))

    published_date = verify_date(published_date)

    b = Book(
        book_id=book_id,
        title=title,
        published_date=published_date,
        average_rating=average_rating,
        ratings_count=ratings_count,
        thumbnail=thumbnail,
    )

    b.save()

    create_and_add_authors(authors, b)
    create_and_add_categories(categories, b)


def update_data_base(value):

    pagination_size = 40  # Maximal size of the google API pagination
    chunk_book_count = pagination_size
    start_index = 0
    chunk_num = 1

    while chunk_book_count == pagination_size:
        items = get_books(value, pagination_size, start_index)

        chunk_book_count = 0

        for book in items:
            chunk_book_count += 1

        start_index += chunk_book_count

        print(f"Loading #{chunk_num} chunk...")

        chunk_num += 1

        for book in tqdm(items):
            create_and_save_book(book)

    print_succes_message()
