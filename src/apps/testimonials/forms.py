from django.forms import ModelForm

from apps.testimonials.models import Testimonial

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

class CEOForm(ModelForm):
    class Meta:
        model = Testimonial
        fields = ('first_name',
              'last_name',
              'city',
              'state',
              'email',
              'experience',
              'department',
              'rep',
              'testimonial',
              'can_post')
    def __init__(self, *args, **kwargs):
        super(CEOForm, self).__init__(*args, **kwargs)
        self.fields['testimonial'].label = 'Feedback'
        self.fields['testimonial'].help_text = 'Please provide as much detailed information as possible regarding the nature of your feedback, especially if you still have an outstanding issue or complaint that you need resolved.'
