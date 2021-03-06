import sys
import random
import csv
from faker import Faker

from django.core.management.base import BaseCommand
from users.models import MarketUser
from market.models import Author, Book, BookRequest, Listing, Transaction
from django.db.utils import IntegrityError
from django.test import override_settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Create some test users
        first_names=['John','Chris','Tom','Jack','Alex','Andrew','David', 'Michael','George','Harry','Sally','Lucy','Sophie','Amy','Carrie','Mary','Jennifer','Caroline','Nancy','Ava']
        last_names=['Smith','Jones','King','Wilsey','White','Bailey','Forte','Green','Blackley','North']

        users = []
        for i in range(30):
            user_first = random.choice(first_names)
            user_last = random.choice(last_names)
            user_name  =user_first+'_'+user_last
            user_email = user_name+'@mail.com'
            try:
                user = MarketUser.objects.create_user(first_name = user_first, last_name = user_last, username = user_name,email = user_email,password = "pass1234")
                user.save()
                users.append(user)
            except:
                print(f"oops, couldn't create {user_name}")

        # Create some listings

        book_conditions=['N','LN','VG','G','F','P']
        comments = ["Great book!","Need asap!","It was just ok","I don't know what the professor was thinking","Very informative"]

        fake = Faker()

        # Find all the books

        books = Book.objects.all()

        # for each book, create a random number of entries, each with a random condition and price

        for book in books:

            with override_settings(USE_TZ=False):
                for i in range(random.randrange(1,10)):
                    user = random.choice(users)
                    date_created=fake.date_between(start_date='-10y', end_date='now')
                    listing = Listing.objects.create(user=user, book=book, price=round(random.uniform(5.0,50.5), 1),
                                                 condition=random.choice(book_conditions),comment=random.choice(comments),
                                                 date_created = date_created)
                    listing.save()
                    if random.choice([True, False]):
                        print("This listing gets a tx")
                        user_b = random.choice(users)

                        while user == user_b:
                            user_b = random.choice(users)

                        transaction = Transaction.objects.create(book=book , seller=user, buyer=(user_b),
                            date_closed=fake.date_between(start_date=date_created, end_date='now'), price=round(random.uniform(5.0,50.5), 1), status=random.randint(1,2))

                        transaction.save()
                        listing.transaction_id = transaction.id
                        listing.save()


                for j in range(random.randrange(1,10)):
                    user = random.choice(users)
                    date_created=fake.date_between(start_date='-10y', end_date='now')
                    book_request = BookRequest.objects.create(user=user, book=book, desired_price=round(random.uniform(5.0,50.5), 1),
                                                 desired_condition=random.choice(book_conditions),comment=random.choice(comments),
                                                 date_created=date_created)
                    book_request.save()
                    if random.choice([True, False]):
                        print("This request gets a tx")
                        user_b = random.choice(users)

                        while user == user_b:
                            user_b = random.choice(users)

                        transaction = Transaction.objects.create(book=book , seller=user_b, buyer=user,
                            date_closed=fake.date_between(start_date=date_created, end_date='now'), price=round(random.uniform(5.0,50.5), 1), status=random.randint(1,2))

                        transaction.save()
                        book_request.transaction_id = transaction.id
                        book_request.save()

            pass
