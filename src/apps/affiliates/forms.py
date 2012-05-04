from django import forms

from apps.affiliates.models import Affiliate, LandingPage

class AddAffiliateForm(forms.ModelForm):
    landing_page = forms.BooleanField(initial=False, required=False,
        help_text='Check this if the Affiliate needs a landing page')


    class Meta:
        model = Affiliate
    
    def clean_agent_id(self):
        super(AddAffiliateForm, self).clean()
        data = self.cleaned_data['agent_id'].lower()
        return data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        
        super(AddAffiliateForm, self).__init__(*args, **kwargs)
        if self.user and not self.user.is_superuser:
            del self.fields['homesite_override']
            del self.fields['use_call_measurement']

        # try to get the landing page
        lp = False
        # print self.instance
        try:
            landingpage = LandingPage.objects.get(affiliate=self.instance)
            lp = True
        except:
            pass
        self.fields['landing_page'].initial = lp
