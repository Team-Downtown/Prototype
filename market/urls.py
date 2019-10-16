from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(), name='books'),
    path('authors/',views.AuthorListView.as_view(), name='authors'),
    path('listings/',views.ListingListView.as_view(), name='listings'),
    path('listings/add/', views.add_listing_check, name='add-listing-check'),
    path('listings/add/<str:isbn>/', views.add_listing, name='add-listing'),
    path('bookrequests/',views.BookRequestListView.as_view(), name='bookrequests'),
    path('bookrequests/add/', views.add_request_check, name='add-request-check'),
    path('bookrequests/add/<str:isbn>/', views.add_request, name='add-request'),
]
