from django import forms
from django.core.exceptions import ValidationError
from . models import Book, Listing, Transaction

class CheckISBNForm(forms.Form):
    isbn = forms.CharField(label='ISBN', min_length=13, max_length=13, strip=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a 13-character ISBN'}),
        error_messages={'required': 'You must enter an ISBN', 'min_length': 'The ISBN must be 13 characters long', 'max_length': 'The ISBN must be 13 characters long'})
    
    def clean_isbn(self):
        data = self.cleaned_data['isbn']
        book = Book.add_if_not_present(data)
        if book is None:
            raise ValidationError('ISBN not found; please try again')
        return data

class AddListingForm(CheckISBNForm):
    price = forms.DecimalField(label_suffix=' $', min_value=0, decimal_places=2,
        error_messages={'required': 'You must enter a price'})
    
    condition = forms.ChoiceField(choices=Listing.BOOK_STATUS,
        error_messages={'required': 'You must enter a condition'})
    
    comments = forms.CharField(required=False, strip=True,
        widget=forms.TextInput(attrs={'placeholder': 'Additional comments (optional)'}))

class AddRequestForm(CheckISBNForm):
    price = forms.DecimalField(label='Desired price', label_suffix=' $', min_value=0, decimal_places=2,
        error_messages={'required': 'You must enter a price'})
    
    condition = forms.ChoiceField(label='Desired condition', choices=Listing.BOOK_STATUS,
        error_messages={'required': 'You must enter a condition'})
    
    comments = forms.CharField(required=False, strip=True,
        widget=forms.TextInput(attrs={'placeholder': 'Additional comments (optional)'}))

class ContactForm(forms.Form):

    # listing_id = forms.IntegerField(       # A hidden input for internal use
    #     widget=forms.HiddenInput(),
    #     initial = 1
    # )
    msg = forms.CharField(required = True,
                                   widget = forms.Textarea
                                   )

class TransactionListingForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status','buyer','price']

class TransactionBookRequestForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status','seller','price']
