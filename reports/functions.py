from users.models import MarketUser
from .models import Listing, Request, Transaction
import numpy as np

def createCSV(model):
#
# num_listings = str(listings.count())
#
# response = HttpResponse(content_type='text/csv')
# response['Content-Disposition'] = 'attachment; filename="listings_report.csv"'
# writer = csv.writer(response, delimiter=',')
#
# write.writerow(num_listings, 'Listings Created between', start, 'and', end)
#
# # header row
# writer.writerow(\
# ['book', 'user', 'condition', 'price', 'comment', 'transaction', 'date_created'])
#
# for l in listings:
#     writer.writerow([l.book, l.user, l.condition, \
#         l.price, l.comment, l.transaction, l.date_created])
#
# return response

def avgsFunc(new_objects, tot_users):

    """ averages """

    avg = new_objects/tot_users # within range
    return avg

def statsFunc(object, start, end):

    ''' avg num per user, mode of num per user, median of num per user '''

    users = MarketUser.objects.all()
    items = [Listing, Request, Transaction]

    # List of counts of each item for each user in range(start, end)
    counts_per_user_list = [item.objects.filter(user=user).filter(date_closed__range=[start, end]).count() \
            for user in users for item in items]

    c = counts_per_user_list

    # con list of lists to numpy array of numpy arrays
    count_per_user = np.array([np.array(ci) for ci in c])

    return count_per_user

    # avg_num_listing_per_user =
    # avg_num_requests_per_user =
    # avg_num_transactions_per_user =
    #
    # mode_num_listing_per_user =
    # mode_num_requests_per_user =
    # mode_num_transactions_per_user =
    #
    # median_num_listing_per_user =
    # median_num_requests_per_user =
    # median_num_transactions_per_user =






    # find the number of items for each user
    # store each number in a list

    return num, mode, median

            # mode, median, avg are all TOTALS PER USER



        #     new_trans, mode_trans, median_trans = countsMedianModeFunc(Transaction, start, end)
        #     new_listings, mode_listings, median_listings = countsMedianModeFunc(Listing, start, end)
        #     new_requests, mode_requests, median_requests = countsMedianModeFunc(MarketUser, start, end)
        #
        #     avg_trans = avgsFunc(new_transaction, tot_users)
        #     avg_listings = avgsFunc(new_listings, tot_users)
        #     avg_requests = avgsFunc(new_requests, tot_users)
        #
        #
        #
        #     csv_data = (('Date Range:', start, 'to', end),
        #                 ('Total Users:', tot_users, '; New Users:' ),
        #                 (''),
        #                 ('Type:', 'Transactions', 'Listings', 'Requests'),
        #                 ('--------------------------------------------------'),
        #                 ('Raw Totals:', num_trans, num_listings, num_requests),
        #                 ('Average Per User:', avg_trans, avg_listings, avg_requests), # avg_price
        #                 ('Mode Per User:', mode_trans, mode_listing, mode_requests ),
        #                 ('Median Per User:', median_trans, median_listings, median_requests),
        #                 ('--------------------------------------------------'),
        #                 ('Total Transactions with Status: Sold on Site:', num_closed_sold_on_site),
        #                 ('Total Transactions with Status: Not Sold on Site:', num_closed_not_sold_on_site)
        #     )
        #     template = loader.get_template('report_template.txt')
        #     content = {'data': csv_data}
        #     response.write(template.render(content))
        #
        #     return HttpResponse(content, content_type='text/plain')
        #
        #
        # else:
        #     form = CreateReportForm()
        #     context = {'create_report_form': form}
        #
        #     return render(request, 'create_report.html', context)
