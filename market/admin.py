from django.contrib import admin
from market.models import Book, Author, Listing, BookRequest, Transaction, UserMessage

admin.site.register(Author)

class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'title', 'display_author', 'publisher', 'published_date')
    #fields = ['isbn', 'title', 'display_author', 'publisher', 'published_date']

#Register the admin class with the associated model
admin.site.register(Book, BookAdmin)

class ListingAdmin(admin.ModelAdmin):
    list_display = ('book','user','condition','price','comment','transaction')

    list_filter = ['condition']

    fields = ['book','user','condition','price','comment','transaction']


admin.site.register(Listing,ListingAdmin)

class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('book','user','desired_condition','desired_price', 'transaction','comment')

    fields = ['book','user','desired_condition','desired_price','comment', 'transaction']

admin.site.register(BookRequest,BookRequestAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book','seller','buyer','date_closed','price')

    fields = ['book','seller','buyer','date_closed','price']

admin.site.register(Transaction, TransactionAdmin)

class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver','date','msg', 'listing_id', 'request_id')
    fields = ['sender','receiver','date','msg', 'listing_id', 'request_id']

admin.site.register(UserMessage, UserMessageAdmin)
