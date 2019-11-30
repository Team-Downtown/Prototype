from django.urls import path
from django.contrib.auth.decorators import permission_required
from . import views

urlpatterns = [
    #path('report/',views.BookRequestSearchResultView.as_view(), name='request_searchresults'),
    path('filter/', views.FilteredTemplateView.as_view(), name='filter'),
    path('totals', views.totals, name='totals'),
    path('requests_by_date/', views.BookRequestFilteredView.as_view(), name='requests-by-date'),
    path('listings_by_date/', views.ListingFilteredView.as_view(), name='listings-by-date'),
    # path('users_by_date/', views.MarketUserFilteredView.as_view(), name='marketusers-by-date'),
    path('transactions_by_date/', views.TransactionFilteredView.as_view(), name='transactions-by-date'),
]
