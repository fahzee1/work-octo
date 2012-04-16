from django import forms

from apps.affiliates.models import Affiliate

class AddAffiliateForm(forms.ModelForm):
    landing_page = forms.BooleanField(initial=False, required=False,
        help_text='Check this if the Affiliate needs a landing page')


    class Meta:
        model = Affiliate
        exclude = ('homesite_override', 'use_call_measurement')

    
    def clean_agent_id(self):
        super(AddAffiliateForm, self).clean()
        data = self.cleaned_data['agent_id'].lower()
        return data
