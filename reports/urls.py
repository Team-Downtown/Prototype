from django.urls import path
from django.contrib.auth.decorators import permission_required
from . import views

urlpatterns = [
    path('create_report/', views.CreateReportView.as_view(), name='create-report'),
    path('user_report/',views.UserReportView.as_view(), name='user-report'),
    path('listing_report/',views.ListingReportView.as_view(), name='listing-report'),
    path('bookrequest_report/',views.BookRequestReportView.as_view(), name='bookrequest-report'),
    path('transaction_report/',views.TransactionReportView.as_view(), name='transaction-report'),
    path('transaction_yes_report/',views.TransactionReportView.as_view(), name='transaction-yes-report'),
    path('transaction_no_report/',views.TransactionReportView.as_view(), name='transaction-no-report'),

]
