from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm
import requests

from books.models import Book, Author, Category
from books import utils


class Command(BaseCommand):
    help = "Updates books database"

    def handle(self, *args, **options):
        utils.update_database("Hobbit")  # Default value for book according to the assignment instructions
