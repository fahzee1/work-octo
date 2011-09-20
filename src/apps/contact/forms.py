import re

from django.forms import ModelForm, Textarea, TextInput, CharField, Select
from django.contrib.localflavor.us.us_states import STATE_CHOICES

from apps.contact.models import Submission

class PAContactForm(ModelForm):
    class Meta:
        model = Submission

        widgets = {
            'name': TextInput(attrs={'placeholder':'Name'}),
            'email': TextInput(attrs={'placeholder':'Email'}),
            'phone': TextInput(attrs={'placeholder':'Phone'}),
            'city': TextInput(attrs={'placeholder':'City',
                'class':'city'}),
            'state': Select(attrs={'class':'state'}),
            'rep_name': TextInput(attrs={
                'placeholder':'Representative\'s Name'}),
            'message': Textarea(attrs={'placeholder':
                'Enter your questions, comments, or concerns here.', 
                'rows':'5'}),
            }


class BasicContactForm(PAContactForm):
    message = CharField(required=True, widget=Textarea(attrs={'placeholder':
                'Enter your questions, comments, or concerns here.',
                'rows':'5'}), )
    department = CharField(required=True, widget=Select(
        choices=Submission.DEPARTMENT_CHOICES))

    class Meta(PAContactForm.Meta):
        fields = ('department', 'name', 'email', 'phone', 'message')

        
class OrderForm(PAContactForm):
    PACKAGE_CHOICES = (
        ('copper', 'Copper'),
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )

    package = CharField(required=True, widget=Select(
        choices=PACKAGE_CHOICES))

    class Meta(PAContactForm.Meta):
        fields = ('name', 'email', 'phone', 'package')


class CeoFeedback(PAContactForm):
    
    # turn states dictionary into a valid CHOICES
    # structure with the postal abbreviation as
    # the value and the verbose name
    STATE_CHOICES_ABBR = [(abbr,abbr) for abbr,state in STATE_CHOICES]

    #d = dict(STATE_CHOICES)
    #STATE_CHOICES_ABBR = zip(d.keys(), d.keys())

    state = CharField(required=True, widget=Select(
        choices=STATE_CHOICES_ABBR, attrs={'class': 'state'}))

    department = CharField(required=True, widget=Select(
        choices=Submission.DEPARTMENT_CHOICES))

    city = CharField(required=True, widget=TextInput(
        attrs={'placeholder':'City', 'class':'city'}))

    class Meta(PAContactForm.Meta):
        fields = ('name', 'email', 'phone', 'city', 'state', 
            'department', 'rep_name', 'message')
