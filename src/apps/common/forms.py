from django import forms

from apps.common.models import LinxContext

class LinxContextForm(forms.ModelForm):
    email_2 = forms.CharField(max_length=128, label="Verify Email")
    class Meta:
        model = LinxContext
        fields = ('name', 'email', 'email_2', 'phone', 'rin')

    def clean(self, *args, **kwargs):
        super(LinxContextForm, self).clean(*args, **kwargs)

        email = self.cleaned_data['email']
        email_2 = self.cleaned_data['email_2']

        if email != email_2:
            raise forms.ValidationError("Your emails do not match.")

        return self.cleaned_data
