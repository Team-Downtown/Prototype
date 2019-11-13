from django.test import TestCase
from django.urls import reverse

from . forms import *
from . models import *


class ModelTests(TestCase):
    @classmethod
    def create_author(cls, name='Test Author 1'):
        author, _ = Author.objects.get_or_create(name=name)
        return author
    
    @classmethod
    def create_book(cls, title='Test Title', isbn='0123456789012',
                    publisher='Test Publisher', published_date='Test Date'):
        book, created = Book.objects.get_or_create(title=title, isbn=isbn,
            publisher=publisher, published_date=published_date)
        if created:
            book.author.add(cls.create_author('Test Author 1'))
            book.author.add(cls.create_author('Test Author 2'))
            book.save()
        return book
    
    @classmethod
    def create_listing(cls, comment='Test listing 1'):
        book = cls.create_book()
        listing, _ = Listing.objects.get_or_create(book=book, comment=comment, price=24)
        return listing
    
    @classmethod
    def create_request(cls, comment='Test request 1'):
        book = cls.create_book()
        request, _ = BookRequest.objects.get_or_create(book=book, comment=comment, desired_price=48)
        return request
        
    def test_author_str(self):
        author = self.create_author()
        self.assertEqual(author.name, str(author))
        
    def test_book_str(self):
        book = self.create_book()
        self.assertEqual(book.title, str(book))
    
    def test_book_display_author(self):
        book = self.create_book()
        display = book.display_author()
        for author in book.author.all():
            self.assertIn(author.name, display)
        
    def test_book_api_working(self):
        Book.add_if_not_present('9781590282410')
        book = Book.objects.get(isbn='9781590282410')
        self.assertEqual(book.isbn, '9781590282410')
        self.assertEqual(book.title, 'Python Programming')


class ViewTests(TestCase):
    def get_response(self, name, kwargs={}):
        url = reverse(name, kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return response
        
    def test_index(self):
        res = self.get_response('index')

    def test_book_list(self):
        book = ModelTests.create_book()
        res = self.get_response('books')
        self.assertIn(book.title, str(res.content))
    
    def test_author_list(self):
        author = ModelTests.create_author()
        res = self.get_response('authors')
        self.assertIn(author.name, str(res.content))
    
    def test_listing_list(self):
        listing = ModelTests.create_listing()
        res = self.get_response('listings')
        self.assertIn(listing.comment, str(res.content))
    
    def test_listing_detail(self):
        listing = ModelTests.create_listing()
        res = self.get_response('listing-detail', {'pk': listing.id})
    
    def test_listing_add_check(self):
        res = self.get_response('add-listing-check')
    
    def test_listing_add(self):
        book = ModelTests.create_book()
        res = self.get_response('add-listing', {'isbn': book.isbn})
    
    def test_listing_contact(self):
        listing = ModelTests.create_listing()
        res = self.get_response('contact-lister', {'id': listing.id})
    
    def test_listing_filter(self):
        listing = ModelTests.create_listing()
        res = self.get_response('listings-by-book', {'isbn': listing.book.isbn})
        self.assertIn(listing.book.title, str(res.content))
    
    def test_request_list(self):
        request = ModelTests.create_request()
        res = self.get_response('bookrequests')
        self.assertIn(request.comment, str(res.content))
    
    def test_request_detail(self):
        request = ModelTests.create_request()
        res = self.get_response('bookrequest-detail', {'pk': request.id})
    
    def test_request_add_check(self):
        res = self.get_response('add-request-check')
    
    def test_request_add(self):
        book = ModelTests.create_book()
        res = self.get_response('add-request', {'isbn': book.isbn})
    
    def test_request_contact(self):
        request = ModelTests.create_request()
        res = self.get_response('contact-requester', {'id': request.id})
    
    def test_request_filter(self):
        request = ModelTests.create_request()
        res = self.get_response('bookrequests-by-book', {'isbn': request.book.isbn})
        self.assertIn(request.book.title, str(res.content))
    
    def test_search(self):
        res = self.get_response('search')
    

class FormTests(TestCase):
    def test_check_isbn_blank(self):
        form = CheckISBNForm()
        self.assertFalse(form.is_valid())
    
    def test_check_isbn_valid(self):
        book = ModelTests.create_book()
        form = CheckISBNForm({
            'isbn': book.isbn,
            })
        self.assertTrue(form.is_valid())
    
    def test_add_listing_blank(self):
        form = AddListingForm()
        self.assertFalse(form.is_valid())
    
    def test_add_listing_valid(self):
        book = ModelTests.create_book()
        form = AddListingForm({
            'isbn': book.isbn,
            'price': 10,
            'condition': 'N',
            })
        self.assertTrue(form.is_valid())
    
    def test_add_request_blank(self):
        form = AddRequestForm()
        self.assertFalse(form.is_valid())
    
    def test_add_request_valid(self):
        book = ModelTests.create_book()
        form = AddRequestForm({
            'isbn': book.isbn,
            'price': 10,
            'condition': 'N',
            })
        self.assertTrue(form.is_valid())
    
    def test_contact_blank(self):
        form = ContactForm()
        self.assertFalse(form.is_valid())
    
    def test_contact_valid(self):
        form = ContactForm({
            'msg': 'Test',
            })
        self.assertTrue(form.is_valid())
