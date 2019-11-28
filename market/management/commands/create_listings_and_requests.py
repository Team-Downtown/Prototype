import sys
import random
import csv

from django.core.management.base import BaseCommand
from users.models import MarketUser
from market.models import Author, Book, BookRequest, Listing, Transaction
from django.db.utils import IntegrityError

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
            except:
                print(f"oops, couldn't create {user_name} for some reason")
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
