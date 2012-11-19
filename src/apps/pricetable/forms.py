from django import forms

from apps.contact.models import EcomLead

class EcomForm(forms.ModelForm):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)

    class Meta:
        model = EcomLead
        fields = ('email',
                  'phone', 
                  'address',
                  'address_2',
                  'city',
                  'state',
                  'zipcode',
                  'consent')