from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(), name='books'),
    path('authors/',views.AuthorListView.as_view(), name='authors'),
    path('listings/',views.ListingListView.as_view(), name='listings'),
    path('listings/<int:pk>',views.ListingDetailView.as_view(), name='listing-detail'),
    path('bookrequests/',views.BookRequestListView.as_view(), name='bookrequests'),
    path('bookrequests/<int:pk>',views.BookRequestDetailView.as_view(), name='bookrequest-detail'),
    path('mylistings/',views.ListingsByUserListView.as_view(), name='my-listings'),
    path('myrequests/',views.RequestsByUserListView.as_view(), name='my-requests'),

]
