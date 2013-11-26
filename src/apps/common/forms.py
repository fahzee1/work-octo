from django import forms

from apps.common.models import LinxContext

class LinxContextForm(forms.ModelForm):
    class Meta:
        model = LinxContext
        fields = ('name', 'email', 'phone', 'rin')


class Unsubscribe(forms.Form):
    unsub_email = forms.EmailField(
        widget=forms.TextInput(attrs={'autofocus': '',
                                      'placeholder': 'user@yourdomain.com'}))
