from django.db import models
import uuid # Required for unique listing instances
from django.contrib.auth import get_user_model
import requests


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

    cover_image = models.URLField(max_length=250, null=True)

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
        """Retrieve information from Google Books, add it to the database if necessary, and return the book.
        
        If the book is not already present in the database nor found by Google Books, return None.
        """
        books = Book.objects.filter(isbn=isbn)
        if books.exists():
            return books[0]
        else:
            response = requests.get('https://www.googleapis.com/books/v1/volumes', params={
                'key': 'AIzaSyBqBgY6u3k6j-UaMtmoOPL0PHAf4pglw3I',
                'q': 'isbn:' + isbn,
            })
            
            if response.status_code == 200:
                j = response.json()
                if 'items' in j and len(j['items']) > 0 and 'volumeInfo' in j['items'][0]:
                    volumeInfo = j['items'][0]['volumeInfo']
                    
                    # Only title is mandatory
                    if 'title' in volumeInfo:
                        title = volumeInfo['title']
                        
                        # Use ISBN from API, if provided
                        if 'industryIndentifiers' in volumeInfo:
                            isbn13 = [x for x in volumeInfo['industryIdentifiers'] if 'type' in x and x['type'] == 'ISBN_13']
                            if len(isbn13) > 0 and 'identifier' in isbn13[0]:
                                isbn = isbn13[0]['identifier']
                        
                        book = Book(isbn=isbn, title=title)
                        
                        if 'publisher' in volumeInfo:
                            book.publisher = volumeInfo['publisher']
                        
                        if 'publishedDate' in volumeInfo:
                            book.published_date = volumeInfo['publishedDate']
                        
                        if 'imageLinks' in volumeInfo and 'thumbnail' in volumeInfo['imageLinks']:
                            book.cover_image = volumeInfo['imageLinks']['thumbnail']
                        
                        # Must be saved before adding authors
                        book.save()
                        if 'authors' in volumeInfo:
                            for name in volumeInfo['authors']:
                                author, _ = Author.objects.get_or_create(name=name)
                                author.save()
                                book.author.add(author)
                        
                        book.save()
                        return book


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

    transaction = models.ForeignKey('Transaction',on_delete=models.SET_NULL, null=True, blank=True, related_name='transaction')

class Transaction(models.Model):

    TX_STATUS = (
        (1, 'Sold in Marketplace'),
        (2, 'Sold outside Marketplace'),
        (3, 'Closed')
    )

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='seller', blank = True, null=True)
    buyer = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='buyer', blank = True, null=True)
    date_closed = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank = True, null=True)
    status = models.IntegerField(
        choices = TX_STATUS,
        default = 1,
    )

class UserMessage(models.Model):

    sender = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='sender', null=True)
    receiver = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='receiver', null=True)
    date = models.DateTimeField(auto_now_add=True)
    #date = models.DateField(auto_now_add=True)
    msg = models.TextField(max_length=200, blank=False)
    listing_id = models.ForeignKey('Listing', on_delete=models.SET_NULL, null=True, blank=True)
    request_id = models.ForeignKey('BookRequest', on_delete=models.SET_NULL, null=True, blank=True)
    parent_id = models.ForeignKey('self',on_delete=models.SET_NULL, null=True,related_name='parent')
    read_flag = models.BooleanField(default = False)

