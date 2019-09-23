from django.contrib import admin
from market.models import Book, Author, Listing, BookRequest, Transaction

admin.site.register(Author)

class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'title', 'display_author', 'publisher', 'published_date')
    #fields = ['isbn', 'title', 'display_author', 'publisher', 'published_date']

#Register the admin class with the associated model
admin.site.register(Book, BookAdmin)

class ListingAdmin(admin.ModelAdmin):
    list_display = ('book','user','condition','price','comment','transaction')

    fields = ['book','user','condition','price','comment','transaction']

admin.site.register(Listing,ListingAdmin)

class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('book','user','desired_condition','desired_price','comment', 'transaction')

    fields = ['book','user','desired_condition','desired_price','comment', 'transaction']

admin.site.register(BookRequest,BookRequestAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book','seller','buyer','date_closed','price')

    fields = ['book','seller','buyer','date_closed','price']

admin.site.register(Transaction, TransactionAdmin)
