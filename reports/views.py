
from django.views import generic
from django.db.models import Q
from django.utils import timezone
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

from users.models import MarketUser
from market.models import Book, Author, Listing, BookRequest, Transaction
from .functions import *

def totals(request):
    '''
    For display for superuser totals.html page of site.

    A. Uses stats_func() from functions.py to calculate:

     (1) Counts
     (2) Average per user
     (3) Mode per user
     (4) Median per

     for Listings, Book Requests, & Transactions

    B. Uses txs1_stats_func() from functions.py to calculate those four stats
     for Transactions with Status Sold on Site

    C. Users txs2_stat_func() from functions.py to calculate those four stats
    for Transactions with Status Not Sold on Site,

    D. And completes some other statistics.
      '''

    num_mus = MarketUser.objects.count()
    num_as = Author.objects.count()
    num_bks = Book.objects.count()

    # avg_price, mode_price, med_price = price_stats_func()

    # listings
    num_ls, avg_ls, med_ls = stats_func(Listing)

    # book requests
    num_brs, avg_brs, med_brs = stats_func(BookRequest)

    # transactions : total
    num_txs, avg_txs, med_txs = stats_func(Transaction)

    # transactions : sold on site
    num_txs1, avg_txs1, med_txs1 = txs1_stats_func(Transaction)

    # transactions : not sold on site
    num_txs2, avg_txs2, med_txs2 = txs2_stats_func(Transaction)

    context = {
        'num_users': num_mus,
        'num_authors': num_as,
        'num_books': num_bks,

        'num_listings': num_ls,
        'avg_ls_per_user': avg_ls,
        'med_ls_per_user': med_ls,

        'num_requests': num_brs,
        'avg_brs_per_user': avg_brs,
        'med_brs_per_user': med_brs,

        'num_transactions': num_txs,
        'avg_txs_per_user': avg_txs,
        'med_txs_per_user': med_txs,

        'num_txs1': num_txs1,
        'avg_txs1_per_user': avg_txs1,
        'med_txs1_per_user': med_txs1,

        'num_txs2': num_txs2,
        'avg_txs2_per_user': avg_txs2,
        'med_txs2_per_user': med_txs2,

    }

    # Render the HTML template totals.html with the data in the context variable
    return render(request, 'reports/totals.html', context=context)

#### added with permission_required to market
# class TransactionListView(generic.ListView):
#     model = Transaction
#     paginate_by = 10
#     template_name='reports/transaction_list.html'

class FilteredTemplateView(generic.TemplateView):
    template_name='reports/filter.html'

class TransactionFilteredView(generic.ListView):
    model = Transaction

    def get_queryset(self):
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')
        filt_txs = Transaction.objects.filter(Q(date_closed__range=[start, end])).all()
        return filt_txs

class BookRequestFilteredView(generic.ListView):
    model = BookRequest

    def get_queryset(self):
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')
        filt_brs = BookRequest.objects.filter(Q(date_created__range=[start, end])).all()
        return filt_brs

class ListingFilteredView(generic.ListView):
    model = Listing

    def get_queryset(self):
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')
        filt_ls = BookListing.objects.filter(Q(date_created__range=[start, end])).all()
        return filt_ls
