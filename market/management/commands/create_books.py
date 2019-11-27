import sys
import random
import csv
import time

from django.core.management.base import BaseCommand
from users.models import MarketUser
from market.models import Author, Book, BookRequest, Listing, Transaction
from django.db.utils import IntegrityError

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('textbooks.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            count = 0
            for row in csv_reader:
                # create the book if it doesn't already exist
                count+=1
                time.sleep(1)
                isbn = row["ISBN"].strip()
                try:

                    print(f"Adding book {count} with isbn {isbn}")
                    Book.add_if_not_present(isbn)
                except Exception as e:
                    print(e)
                    print(f"ISBN {isbn} failed")

