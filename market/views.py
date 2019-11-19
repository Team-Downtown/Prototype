from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from . forms import CheckISBNForm, AddListingForm, AddRequestForm, ContactForm, TransactionListingForm, TransactionBookRequestForm
from . models import Book, Author, Listing, BookRequest, UserMessage, Transaction

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    book_list = Book.objects.order_by("title")[:5]
    num_books = Book.objects.all().count()
    num_listings = Listing.objects.all().count()
    num_requests = BookRequest.objects.all().count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'book_list': book_list,
        'num_books': num_books,
        'num_listings': num_listings,
        'num_authors': num_authors,
        'num_requests':num_requests,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class AuthorListView(generic.ListView):
    model = Author


class ListingListView(generic.ListView):
    model = Listing
    paginate_by = 10
    ordering = ['book__title']

    def get_queryset(self):
        return Listing.objects.filter(transaction = None)


class BookRequestListView(generic.ListView):
    model = BookRequest
    paginate_by = 10
    ordering = ['book__title']

    def get_queryset(self):
        return BookRequest.objects.filter(transaction = None)


class ListingsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Listing
    template_name = 'market/listings_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Listing.objects.filter(user = self.request.user).order_by('transaction_id')


class RequestsByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookRequest
    template_name = 'market/requests_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookRequest.objects.filter(user = self.request.user).order_by('transaction_id')

class UserMessagesByUserListView(LoginRequiredMixin, generic.ListView):
    model = UserMessage
    template_name = 'market/messages_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return UserMessage.objects.filter(Q(receiver = self.request.user)|Q(sender = self.request.user)).order_by('-date')
      #  return UserMessage.objects.all()

class SearchView(generic.TemplateView):
    template_name = 'market/search.html'

class ListingSearchResultView(generic.ListView):
    model = Listing

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Listing.objects.filter\
            ( Q(book__title__icontains=query) | Q(book__isbn__icontains=query) )
        return object_list

class BookRequestSearchResultView(generic.ListView):
    model = BookRequest

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = BookRequest.objects.filter\
            ( Q(book__title__icontains=query) | Q(book__isbn__icontains=query) )
        return object_list

class ListingDetailView(generic.DetailView):
    model = Listing


class BookRequestDetailView(generic.DetailView):
    model = BookRequest

class UserMessageDetailView(LoginRequiredMixin,generic.DetailView):
    model = UserMessage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.object.listing_id!=None):
            context['msg_context'] = "Listing ID "+str(self.object.listing_id.id)+" - "+self.object.listing_id.book.title
            context['cover_image'] = self.object.listing_id.book.cover_image
        elif (self.object.request_id!=None):
            context['msg_context'] = "Request ID "+str(self.object.request_id.id)+" - "+self.object.request_id.book.title
            context['cover_image'] = self.object.request_id.book.cover_image
        # Possibly decrement unread messages count here??
        if self.object.read_flag == False:
            if self.object.receiver.unreadMessages!=0:
                self.object.receiver.unreadMessages-=1
                self.object.receiver.save()
            self.object.read_flag = True
            self.object.save()
        return context

class ListingUpdate(generic.UpdateView):
    model = Listing
    template_name_suffix = '_update_form'
    fields = ('price','condition','comment')
    success_url = '/marketplace/mylistings/'

def create_listing_transaction(request, id = None):
    if id is not None:
        listing = get_object_or_404(Listing, id = id)
    else:
        listing = None
    form = TransactionListingForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.seller = request.user
        if listing is not None:
            instance.book = listing.book
        instance.save()
        if listing is not None:
            listing.transaction_id = instance.id
            listing.save()
        return HttpResponseRedirect(reverse('my-listings'))

    else:
        form = TransactionListingForm()

        context = {
        'form': form,
         }
    return render(request, 'market/create_transaction.html', context)

def create_bookrequest_transaction(request, id = None):
    if id is not None:
        book_request = get_object_or_404(BookRequest, id = id)
    else:
        listing = None
    form = TransactionBookRequestForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.buyer = request.user
        if book_request is not None:
            instance.book = book_request.book
        instance.save()
        if book_request is not None:
            book_request.transaction_id = instance.id
            book_request.save()
        return HttpResponseRedirect(reverse('my-requests'))

    else:
        form = TransactionBookRequestForm()

        context = {
        'form': form,
         }
    return render(request, 'market/create_transaction.html', context)

@login_required
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

@login_required
def add_listing(request, isbn):
    if request.method == 'POST':
        form = AddListingForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            condition = form.cleaned_data['condition']
            comment = form.cleaned_data['comments']

            book = Book.objects.get(isbn=isbn)
            user = None
            if request.user.is_authenticated:
                user = request.user
            listing = Listing(price=price, condition=condition, comment=comment, book=book,user = user)
            listing.save()
            return HttpResponseRedirect(reverse('listing-detail', args=(listing.id,)))

    else:
        form = AddListingForm(initial={'isbn': isbn})

    context = {
        'add_listing_form': form,
    }
    return render(request, 'market/add_listing.html', context)

@login_required
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

@login_required
def add_request(request, isbn):
    if request.method == 'POST':
        form = AddRequestForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            condition = form.cleaned_data['condition']
            comment = form.cleaned_data['comments']

            book = Book.objects.get(isbn=isbn)
            user = None
            if request.user.is_authenticated:
                user = request.user
            req = BookRequest(desired_price=price, desired_condition=condition, comment=comment, book=book, user=user)
            req.save()
            return HttpResponseRedirect(reverse('bookrequest-detail', args=(req.id,)))

    else:
        form = AddRequestForm(initial={'isbn': isbn})

    context = {
        'add_request_form': form,
    }
    return render(request, 'market/add_request.html', context)

def contact_lister(request, id):

    listing = Listing.objects.get(id=id)

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            msg = form.cleaned_data['msg']
            usermsg = UserMessage(sender=request.user, receiver = listing.user,msg=msg,listing_id=listing)
            usermsg.save()
            # Possibly increment unread message count here? Need to worry about race conditions?
            listing.user.unreadMessages+=1
            listing.user.save()
            return HttpResponseRedirect('/')

    else:
        form = ContactForm()

    return render(request,'market/contact_lister.html', {
        'form':form, 'listing':listing})

def contact_requester(request, id):

    bookrequest = BookRequest.objects.get(id=id)

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            msg = form.cleaned_data['msg']
            usermsg = UserMessage(sender=request.user, receiver = bookrequest.user,msg=msg,request_id=bookrequest)
            usermsg.save()
            bookrequest.user.unreadMessages+=1
            bookrequest.user.save()
            return HttpResponseRedirect('/')

    else:
        form = ContactForm()

    return render(request,'market/contact_requester.html', {
        'form':form, 'bookrequest':bookrequest})

def respond_to_message(request, id):

    usermessage = UserMessage.objects.get(id=id)

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            msg = form.cleaned_data['msg']
            usermsg = UserMessage(sender=usermessage.receiver, receiver =usermessage.sender,msg=msg,listing_id=usermessage.listing_id,
                                  parent_id = usermessage)
            usermsg.save()
            # Need to increment unread count
            usermessage.sender.unreadMessages+=1
            usermessage.sender.save()
            return HttpResponseRedirect('/')

    else:
        form = ContactForm()

    return render(request,'market/respond_to_message.html', {
        'form':form, 'usermessage':usermessage})

def getListingsByBook(request, isbn):
    books = Listing.objects.filter(book = isbn)
    return render(request,'market/listing_list.html', {'listing_list':books})

def getBookRequestsByBook(request, isbn):
    books = BookRequest.objects.filter(book = isbn)
    return render(request,'market/bookrequest_list.html', {'bookrequest_list':books})
