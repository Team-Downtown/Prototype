import sys
import random
import csv

from django.core.management.base import BaseCommand
from users.models import MarketUser
from market.models import Author, Book, BookRequest, Listing, Transaction
from django.db.utils import IntegrityError

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('books.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # create the book if it doesn't already exist
                isbn = row["ISBN"].strip()
                Book.add_if_not_present(isbn)

        # Create some test users
        users = []
        for i in range(10):
            user_name='user_'+str(i)
            user_email = user_name+'@mail.com'
            user = MarketUser.objects.create_user(user_name,user_email,"pass1234")
            user.save()
            users.append(user)

        # Create some listings

        book_conditions=['N','LN','VG','G','F','P']
        comments = ["Great book!","Need asap!","It was just ok","I don't know what the professor was thinking","Very informative"]

        # Find all the books

        books = Book.objects.all()

        # for each book, create a random number of entries, each with a random condition and price

        for book in books:
            for i in range(random.randrange(1,10)):
                listing = Listing.objects.create(user=random.choice(users), book=book, price=round(random.uniform(5.0,50.5), 1),
                                             condition=random.choice(book_conditions),comment=random.choice(comments))
                listing.save()

            for j in range(random.randrange(1,10)):
                book_request = BookRequest.objects.create(user=random.choice(users), book=book, desired_price=round(random.uniform(5.0,50.5), 1),
                                             desired_condition=random.choice(book_conditions),comment=random.choice(comments))
                book_request.save()
