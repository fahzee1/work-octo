from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('apps.testimonials.views',
    url(r'^api/post/?$', 'post_testimonial', name="post_testimonial"),
)
