from django.shortcuts import render

from market.models import Book, Author, Listing, BookRequest

from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin

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
    paginate_by = 10

class BookRequestListView(generic.ListView):
    model = BookRequest
    paginate_by = 10

class ListingsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Listing
    template_name = 'market/listings_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Listing.objects.filter(user = self.request.user)

class RequestsByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookRequest
    template_name = 'market/requests_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookRequest.objects.filter(user = self.request.user)

class ListingDetailView(generic.DetailView):
    model = Listing
