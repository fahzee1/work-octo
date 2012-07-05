import re

from django.forms import ModelForm, Textarea, TextInput, CharField, Select
from django.contrib.localflavor.us.us_states import STATE_CHOICES

from apps.contact.models import (Submission,
                                 CEOFeedback,
                                 DEPARTMENT_CHOICES,
                                 ContactUs, 
                                 MovingKit,
                                 TellAFriend)

class PAContactForm(ModelForm):
    class Meta:
        model = Submission

        widgets = {
            'name': TextInput(attrs={'placeholder':'Name'}),
            'email': TextInput(attrs={'placeholder':'Email'}),
            'phone': TextInput(attrs={'placeholder':'Phone'}),
            'city': TextInput(attrs={'class':'city'}),
            'state': Select(attrs={'class':'state'}),
            'rep_name': TextInput(),
            'message': Textarea(attrs={'placeholder':
                'Enter your questions, comments, or concerns here.', 
                'rows':'5'}),
            }


class AffiliateLongForm(PAContactForm):
    class Meta(PAContactForm.Meta):
        fields = ('name',
                  'email',
                  'phone',
                  'address',
                  'city',
                  'state',
                  'zipcode',
                  'homeowner',
                  'creditrating',
                  'consent')

        widgets = {
            'name': TextInput(attrs={'placeholder':'Name'}),
            'email': TextInput(attrs={'placeholder':'Email'}),
            'phone': TextInput(attrs={'placeholder':'Phone'}),
            'city': TextInput(attrs={'class':'city', 'placeholder': 'City'}),
            'state': TextInput(attrs={'placeholder': 'State'}),
            'zipcode': TextInput(attrs={'placeholder':'Zipcode'}),
            'address': TextInput(attrs={'placeholder':'Street Address'}),
        }
        
class OrderForm(PAContactForm):
    PACKAGE_CHOICES = (
        ('copper', 'Copper'),
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('business', 'Business'),

    )

    package = CharField(required=True, widget=Select(
        choices=PACKAGE_CHOICES))

    class Meta(PAContactForm.Meta):
        fields = ('name', 'email', 'phone', 'package')


class MovingKitForm(ModelForm):
    class Meta:
        model = MovingKit
    def __init__(self, *args, **kwargs):
        super(MovingKitForm, self).__init__(*args, **kwargs)
        self.fields['current_state'].widget.attrs['class'] = 'state'
        self.fields['current_city'].widget.attrs['class'] = 'city'
        self.fields['current_zipcode'].widget.attrs['class'] = 'zip'

        self.fields['new_state'].widget.attrs['class'] = 'state'
        self.fields['new_city'].widget.attrs['class'] = 'city'
        self.fields['new_zipcode'].widget.attrs['class'] = 'zip'

        self.fields['shipping_state'].widget.attrs['class'] = 'state'
        self.fields['shipping_city'].widget.attrs['class'] = 'city'
        self.fields['shipping_zipcode'].widget.attrs['class'] = 'zip'

class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUs

class CeoFeedbackForm(ModelForm):
    class Meta:
        model = CEOFeedback

    def __init__(self, *args, **kwargs):
        super(CeoFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['id'] = 'state'
        self.fields['city'].widget.attrs['class'] = 'city'
    
class TellAFriendForm(ModelForm):
    class Meta:
        model = TellAFriend