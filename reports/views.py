import csv
from django.shortcuts import render, HttpResponse
from django.views import generic
from django.db.models import Q
from django.utils import timezone
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

from users.models import MarketUser
from market.models import Listing, BookRequest, Transaction



class CreateReportView(generic.TemplateView):
    template_name = 'reports/create_report.html'

class ListingReportView(generic.ListView):
    model = Listing

    def get_queryset(self):
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')

        listings = Listing.objects.filter(Q(date_created__range=[start, end]))

        return listings

class BookRequestReportView(generic.ListView):
    model = BookRequest

    def get_queryset(self):
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')

        requests = BookRequest.objects.filter(Q(date_created__range=[start, end]))

        return requests


class TransactionReportView(generic.ListView):
    model =  Transaction

    def get_queryset(self):
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')

        transactions =  Transaction.objects.filter(Q(date_closed__range=[start, end]))

        return transactions

class UserReportView(generic.ListView):
    model = MarketUser

    def get_queryset(self):
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')

        users = MarketUser.objects.filter(Q(date_joined__range=[start, end]))

        return users
