from django.forms import ModelForm, ValidationError

from apps.testimonials.models import Testimonial, Textimonial

class TestimonialForm(ModelForm):
    class Meta:
        model = Testimonial
        fields = ('first_name',
                  'last_name',
                  'city',
                  'state',
                  'email',
                  'experience',
                  'testimonial',
                  'can_post')

    def __init__(self, *args, **kwargs):
        # Only allow Positive or Negative feedback options
        super(TestimonialForm, self).__init__(*args, **kwargs)
        EXPERIENCE_CHOICES = (
            ('POSITIVE', 'Positive Feedback'),
            ('NEGATIVE', 'Negative Feedback'),
        )
        self.fields['experience'].choices = EXPERIENCE_CHOICES
        self.fields['email'].help_text = 'If you would like to have a way for Protect America to contact you please leave your email'

class TextimonialForm(ModelForm):
    class Meta:
      model = Textimonial

    def __init__(self, *args, **kwargs):
        # Only allow Positive or Negative feedback options
        super(TextimonialForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'half-box alpha'
        self.fields['last_name'].widget.attrs['class'] = 'half-box omega'
        self.fields['city'].widget.attrs['class'] = 'half-box'
        self.fields['message'].label = 'Your Testimonial'