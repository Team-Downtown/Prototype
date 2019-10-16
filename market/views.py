from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from . forms import CheckISBNForm, AddListingForm, AddRequestForm
from . models import Book, Author, Listing, BookRequest

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_listings = Listing.objects.all().count()
    num_requests = BookRequest.objects.all().count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_listings': num_listings,
        'num_authors': num_authors,
        'num_requests':num_requests,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class ListingListView(generic.ListView):
    model = Listing


class BookRequestListView(generic.ListView):
    model = BookRequest


def add_listing_check(request):
    if request.method == 'POST':
        form = CheckISBNForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('add-listing', args=(form.cleaned_data['isbn'],)))
    
    else:
        form = CheckISBNForm()
        
    context = {
        'check_isbn_form': form,
    }
    return render(request, 'market/add_listing_check.html', context)


def add_listing(request, isbn):
    if request.method == 'POST':
        form = AddListingForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            condition = form.cleaned_data['condition']
            comment = form.cleaned_data['comments']
            
            book = Book.objects.get(isbn=isbn)
            listing = Listing(price=price, condition=condition, comment=comment, book=book)
            listing.save()
            return HttpResponseRedirect(reverse('listings'))
    
    else:
        form = AddListingForm(initial={'isbn': isbn})
    
    context = {
        'add_listing_form': form,
    }
    return render(request, 'market/add_listing.html', context)

def add_request_check(request):
    if request.method == 'POST':
        form = CheckISBNForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('add-request', args=(form.cleaned_data['isbn'],)))
    
    else:
        form = CheckISBNForm()
        
    context = {
        'check_isbn_form': form,
    }
    return render(request, 'market/add_request_check.html', context)


def add_request(request, isbn):
    if request.method == 'POST':
        form = AddRequestForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            condition = form.cleaned_data['condition']
            comment = form.cleaned_data['comments']
            
            book = Book.objects.get(isbn=isbn)
            req = BookRequest(desired_price=price, desired_condition=condition, comment=comment, book=book)
            req.save()
            return HttpResponseRedirect(reverse('bookrequests'))
    
    else:
        form = AddRequestForm(initial={'isbn': isbn})
    
    context = {
        'add_request_form': form,
    }
    return render(request, 'market/add_request.html', context)