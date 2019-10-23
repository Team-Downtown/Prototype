from django import forms
from django.core.exceptions import ValidationError
from . models import Book, Listing

class CheckISBNForm(forms.Form):
    isbn = forms.CharField(label='ISBN', empty_value='Enter a 13-character ISBN', min_length=13, max_length=13, strip=True,
        error_messages={'required': 'You must enter an ISBN', 'min_length': 'The ISBN must be 13 characters long', 'max_length': 'The ISBN must be 13 characters long'})
    
    def clean_isbn(self):
        data = self.cleaned_data['isbn']
        Book.add_if_not_present(data)
        if not Book.objects.filter(isbn=data).exists():
            raise ValidationError('ISBN not found; please try again')
        return data

class AddListingForm(CheckISBNForm):
    price = forms.DecimalField(label_suffix=' $', min_value=0, decimal_places=2,
        error_messages={'required': 'You must enter a price'})
    
    condition = forms.ChoiceField(choices=Listing.BOOK_STATUS,
        error_messages={'required': 'You must enter a condition'})
    
    comments = forms.CharField(empty_value='Additional comments (optional)', required=False, strip=True)

class AddRequestForm(CheckISBNForm):
    price = forms.DecimalField(label='Desired price', label_suffix=' $', min_value=0, decimal_places=2,
        error_messages={'required': 'You must enter a price'})
    
    condition = forms.ChoiceField(label='Desired condition', choices=Listing.BOOK_STATUS,
        error_messages={'required': 'You must enter a condition'})
    
    comments = forms.CharField(empty_value='Additional comments (optional)', required=False, strip=True)