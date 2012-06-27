from django import forms

from apps.affiliates.models import Affiliate, LandingPage, Profile

class AddAffiliateForm(forms.ModelForm):
    landing_page = forms.BooleanField(initial=False, required=False,
        help_text='Check this if the Affiliate needs a landing page')


    class Meta:
        model = Affiliate
    
    def clean_agent_id(self):
        super(AddAffiliateForm, self).clean()
        data = self.cleaned_data['agent_id']
        if not self.user.is_superuser:
            data = self.cleaned_data['agent_id'].lower()
        return data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        
        super(AddAffiliateForm, self).__init__(*args, **kwargs)
        if self.user and not self.user.is_superuser:
            del self.fields['homesite_override']
            del self.fields['use_call_measurement']
            del self.fields['thank_you']

        # try to get the landing page
        lp = False
        # print self.instance
        try:
            landingpage = LandingPage.objects.get(affiliate=self.instance)
            lp = True
        except:
            pass
        self.fields['landing_page'].initial = lp

class AffiliateSignup(forms.ModelForm):
    
    class Meta:
        model = Profile

        fields = ('name',
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
                  'website',
                  'comments',
                  'agreed_to_terms',
                  'sign')

    def __init__(self, *args, **kwargs):
        super(AffiliateSignup, self).__init__(*args, **kwargs)

        self.fields['agreed_to_terms'].widget.attrs['class'] = 'checkbox'
