# Forms for crm 
from django import forms
from django.contrib.auth.models import User, Group

from apps.affiliates.models import Affiliate, LandingPage, Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("This user does not exist.")

        return username

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'span4'
        self.fields['password'].widget.attrs['class'] = 'span4'

class AffiliateForm(forms.ModelForm):

    has_landing_page = forms.BooleanField(initial=False, required=False,
        help_text="Enable this if you would like to equip your affiliate \
        with a landing page.")

    class Meta:
        model = Affiliate

        fields = ('agent_id', 'name', 'phone', 'has_landing_page',
            'pixels', 'conversion_pixels', 'manager')

    def clean_agent_id(self):
        agent_id = self.cleaned_data.get('agent_id', None)
        return agent_id.lower()

    def __init__(self, *args, **kwargs):
        super(AffiliateForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance:
            if instance.has_landing_page():
                self.fields['has_landing_page'].initial = True
        affiliate_group = Group.objects.get(name="AFFILIATE")
        users = User.objects.filter(groups=affiliate_group)
        self.fields['manager'].queryset = users

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            'title',
            'company_name',
            'taxid',
            'street_address',
            'city',
            'state',
            'zipcode',
            'phone',
            'fax',
            'email',
            'website'
        )