from django.urls import path, include
from . import views
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(), name='books'),
    path('authors/',views.AuthorListView.as_view(), name='authors'),
    path('listings/',views.ListingListView.as_view(), name='listings'),
    path('listings/<int:pk>',views.ListingDetailView.as_view(), name='listing-detail'),
    path('listings/add/', views.add_listing_check, name='add-listing-check'),
    path('listings/add/<str:isbn>/', views.add_listing, name='add-listing'),
    path('bookrequests/',views.BookRequestListView.as_view(), name='bookrequests'),
    path('bookrequests/<int:pk>',views.BookRequestDetailView.as_view(), name='bookrequest-detail'),
    path('bookrequests/add/', views.add_request_check, name='add-request-check'),
    path('bookrequests/add/<str:isbn>/', views.add_request, name='add-request'),
    path('mylistings/',views.ListingsByUserListView.as_view(), name='my-listings'),
    path('myrequests/',views.RequestsByUserListView.as_view(), name='my-requests'),
    path('mymessages/',views.UserMessagesByUserListView.as_view(), name='my-user-messages'),
    path('mymessages/<int:pk>',views.UserMessageDetailView.as_view(), name='usermessage-detail'),
    path('listings/contact/<int:id>', views.contact_lister, name='contact-lister'),
    path('bookrequests/contact/<int:id>', views.contact_requester, name='contact-requester'),
    path('mymessages/respond/<int:id>',views.respond_to_message, name='respond-to-message'),
    path('listingsearch/',views.ListingSearchResultView.as_view(), name='listing_searchresults'),
    path('requestsearch/',views.BookRequestSearchResultView.as_view(), name='request_searchresults'),
    path('search/',views.SearchView.as_view(), name='search'),
    path('listings/filter/<str:isbn>',views.getListingsByBook, name='listings-by-book'),
    path('bookrequests/filter/<str:isbn>',views.getBookRequestsByBook, name='bookrequests-by-book'),
    path('mylistings/update/<int:pk>',views.ListingUpdate.as_view(), name='update-listing'),
    path('mylistings/transaction/<int:id>',views.create_listing_transaction, name='create-listing-transaction'),
    path('myrequests/transaction/<int:id>',views.create_bookrequest_transaction, name='create-request-transaction'),
    path('transactions/', permission_required(views.TransactionListView.as_view()), name='transactions'),
    # path('transactions/', permission_required('market.transaction'), views.TransactionListView.as_view(), name='transactions'),
]
