from django.db import models
import uuid # Required for unique listing instances
from django.contrib.auth import get_user_model


class Author(models.Model):
    """Model representing an author."""
    name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """ Model representing a book (but not a specific copy of a book."""
    title = models.CharField(max_length=200)

    author = models.ManyToManyField(Author)

    isbn = models.CharField('ISBN', primary_key=True, max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    publisher = models.CharField('Publisher', max_length=50, null=True, blank=True)

    # do we want to store this as a DateField or a CharField??
    published_date = models.CharField('Published Date', max_length=20, null=True, blank=True)

    def __str__(self):
        """"String for representing the Model object."""
        return self.title

    # def get_absolute_url(self):
    #     """ Returns the url to access a detail record for this book."""
    #     return reverse('book-detail', args = [str(self.id)])

    def display_author(self):

        return ', '.join(author.name for author in self.author.all()[:3])

    display_author.short_description = 'Author'

    @classmethod
    def add_if_not_present(cls, isbn):
        if not Book.objects.filter(isbn=isbn).exists():
            response = requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': 'isbn:' + isbn})
            if response.status_code == 200:
                j = response.json()
                if j['totalItems'] > 0:
                    volumeInfo = j['items'][0]['volumeInfo']
                    isbn = next(ident['identifier'] for ident in volumeInfo['industryIdentifiers'] if ident['type'] == 'ISBN_13')
                    title = volumeInfo['title']
                    published_date = volumeInfo['publishedDate']

                    book = Book(isbn=isbn, title=title, published_date=published_date)
                    book.save()

                    for name in volumeInfo['authors']:
                        author, _ = Author.objects.get_or_create(name=name)
                        author.save()
                        book.author.add(author)
                        book.save()


class Listing(models.Model):

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, null=True)

    BOOK_STATUS = (
        ('N', 'New'),
        ('LN', 'Like New'),
        ('VG', 'Very Good'),
        ('G', 'Good'),
        ('F', 'Fair'),
        ('P', 'Poor'),
    )

    condition = models.CharField(
        max_length=2,
        choices=BOOK_STATUS,
        default='G',
        help_text='Book condition',
    )

    price = models.DecimalField(max_digits=6, decimal_places=2)

    comment = models.TextField(max_length=200,  blank=True)
    transaction = models.ForeignKey('Transaction',on_delete=models.SET_NULL, null=True, blank=True)

class BookRequest(models.Model):

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular request across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, null=True)

    BOOK_STATUS = (
        ('N', 'New'),
        ('LN', 'Like New'),
        ('VG', 'Very Good'),
        ('G', 'Good'),
        ('F', 'Fair'),
        ('P', 'Poor'),
    )

    desired_condition = models.CharField(
        max_length=2,
        choices=BOOK_STATUS,
        default='G',
        help_text='Book condition',
    )

    desired_price = models.DecimalField(max_digits=6, decimal_places=2)

    comment = models.TextField(max_length=200, blank=True)

    transaction = models.ForeignKey('Transaction',on_delete=models.SET_NULL, null=True, blank=True)

class Transaction(models.Model):

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='seller', null=True)
    buyer = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='buyer', null=True)
    date_closed = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

# class UserMessage(models.Model):
#
#     sender = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='sender', null=False)
#     receiver = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='receiver', null=False)
#     date = models.DateField(auto_now_add=True)
#     msg = models.TextField(max_length=200, blank=False)

