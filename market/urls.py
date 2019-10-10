from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(), name='books'),
    path('authors/',views.AuthorListView.as_view(), name='authors'),
    path('listings/',views.ListingListView.as_view(), name='listings'),
    path('bookrequests/',views.BookRequestListView.as_view(), name='bookrequests'),
]
