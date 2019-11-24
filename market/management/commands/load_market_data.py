import sys
import random
import csv

from django.core.management.base import BaseCommand
from users.models import MarketUser
from market.models import Author, Book, BookRequest, Listing, Transaction
from django.db.utils import IntegrityError
from django.test import override_settings
from datetime import date, datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('books.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # create the book if it doesn't already exist
                isbn = row["ISBN"].strip()
                Book.add_if_not_present(isbn)

        superuser = MarketUser.objects.create_superuser(
            username='textbook',
            email='textbook@mail.com',
            password='capstone')

        superuser.save()

        # Create some test users
        users = []
        for i in range(20):
            user_name='user_'+str(i)
            user_email = user_name+'@mail.com'
            user = MarketUser.objects.create_user(user_name,user_email,"pass1234")
            user.save()
            users.append(user)

        # Create some listings

        book_conditions=['N','LN','VG','G','F','P']
        comments = ["Great book!","Need asap!","It was just ok","I don't know what the professor was thinking","Very informative"]

        dates = []
        for i in range(20): # generate 20 random dates
            mo = random.randint(1, 12)
            day = random.randint(1, 28)
            yr = random.randint(2014, 2019)
            dates.append(date(yr, mo, day))

        # Find all the books

        books = Book.objects.all()

        # for each book, create a random number of entries, each with a random condition price

        for book in books:

            with override_settings(USE_TZ=False):

                for i in range(random.randrange(1,10)):
                    listing = Listing.objects.create(user=random.choice(users), book=book, price=round(random.uniform(5.0,50.5), 1),
                                                 condition=random.choice(book_conditions),comment=random.choice(comments),
                                                 date_created=random.choice(dates))
                    listing.save()

                for j in range(random.randrange(1,10)):
                    book_request = BookRequest.objects.create(user=random.choice(users), book=book, desired_price=round(random.uniform(5.0,50.5), 1),
                                                 desired_condition=random.choice(book_conditions),comment=random.choice(comments),
                                                 date_created=random.choice(dates))
                    book_request.save()

                for k in range(random.randrange(1, 10)):

                    user_s = random.choice(users)
                    user_b = random.choice(users)
                    while user_s == user_b:
                        user_b = random.choice(users)

                    transaction = Transaction.objects.create(book=book , seller=(user_s), buyer=(user_b),
                        date_closed=random.choice(dates), price=round(random.uniform(5.0,50.5), 1), status=random.randint(1,3))

                    transaction.save()
            pass
