import csv
from users.models import MarketUser
from market.models import Listing, BookRequest, Transaction
import numpy as np
from django.shortcuts import render, HttpResponse

def stats_func(item):

    # list of Market Users
    users = MarketUser.objects.all()

    # Count of Item
    count = item.objects.count()

    # List of Counts of Items per User
    if item == Transaction:
        user_counts = [item.objects.filter(seller=u).count() for u in users]
    else:
        user_counts = [item.objects.filter(user=u).count() for u in users]

    # Average, Mode, Median Counts of Items per user
    avg_count_items_per_user = np.mean(user_counts)
    median_count_items_per_user = np.median(user_counts)

    return count, avg_count_items_per_user, median_count_items_per_user

def txs1_stats_func(tx):

    # list of Market Users
    users = MarketUser.objects.all()

    count = tx.objects.filter(status=1).count()

    # List of Counts of Items per User
    user_counts = [tx.objects.filter(seller=u).filter(status=1).count() for u in users]

    # Average, Mode, Median Counts of Items per user
    avg_count_items_per_user = np.mean(user_counts)
    median_count_items_per_user = np.median(user_counts)

    return count, avg_count_items_per_user, median_count_items_per_user

def txs2_stats_func(tx):

    # list of Market Users
    users = MarketUser.objects.all()

    count = tx.objects.filter(status=2).count()

    # List of Counts of Items per User
    user_counts = [tx.objects.filter(seller=u).filter(status=2).count() for u in users]

    # Average, Mode, Median Counts of Items per user
    avg_count_items_per_user = np.mean(user_counts)
    median_count_items_per_user = np.median(user_counts)

    return count, avg_count_items_per_user, median_count_items_per_user
