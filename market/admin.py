from django.contrib import admin
from market.models import Book, Author, Listing, BookRequest, Transaction, UserMessage
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from import_export import resources

#Register the admin class with the associated model
admin.site.register(Author)

### ABSTRACT BASE CLASS - for data export

class ExportMixinAdmin(ExportMixin, admin.ModelAdmin):
    def get_export_formats(self):
        ''' excludes YAML file type '''
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
              base_formats.TSV,
              base_formats.ODS,
              base_formats.JSON,
              base_formats.HTML,
              )
        return [f for f in formats if f().can_export()]

    class Meta:
        abstract = True


### BOOK ADMIN

class BookResource(resources.ModelResource):
    ''' used to overwrite defaults in ExportMixinAdmin class'''

    class Meta:
        model = Book
        import_id_fields = ('isbn',) # uses isbn as id
        fields = ('isbn', 'title', 'display_author', 'publisher', 'published_date',)

class BookAdmin(ExportMixinAdmin):
    list_display = ('isbn', 'title', 'display_author', 'publisher', 'published_date')
    #fields = ('isbn', 'title', 'display_author', 'publisher', 'published_date')
    resource_class = BookResource

admin.site.register(Book, BookAdmin)


### LISTING ADMIN

class ListingAdmin(ExportMixinAdmin):
    list_display = ('book','user','condition','price','comment','transaction', 'date_created')
    list_filter = ['condition']
    fields = ['book','user','condition','price','comment','transaction', 'date_created']

admin.site.register(Listing,ListingAdmin)

class BookRequestAdmin(ExportMixinAdmin):
    list_display = ('book','user','desired_condition','desired_price', 'transaction','comment', 'date_created')

    fields = ['book','user','desired_condition','desired_price','comment', 'transaction', 'date_created']

admin.site.register(BookRequest,BookRequestAdmin)


### TRANSACTION ADMIN

class TransactionAdmin(ExportMixinAdmin):
    list_display = ('book','seller','buyer','date_closed','price')

    fields = ['book','seller','buyer','date_closed','price']

admin.site.register(Transaction, TransactionAdmin)

#class UserMessageAdmin(admin.ModelAdmin):
class UserMessageAdmin(ExportMixinAdmin):
    list_display = ('sender','receiver','date','msg', 'listing_id', 'request_id')
    fields = ['sender','receiver','date','msg', 'listing_id', 'request_id']

admin.site.register(UserMessage, UserMessageAdmin)
