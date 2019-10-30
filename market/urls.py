from django.urls import path, include
from . import views

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
    path('listingsearch/',views.ListingSearchResultView.as_view(), name='listing_searchresults'),
    path('requestsearch/',views.BookRequestSearchResultView.as_view(), name='request_searchresults'),
    path('search/',views.SearchView.as_view(), name='search'),
]
